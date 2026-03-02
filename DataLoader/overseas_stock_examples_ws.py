import sys
import logging

import pandas as pd

sys.path.extend(['..', '.'])
import kis_auth as ka
from overseas_stock_functions_ws import *

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 인증
ka.auth()
ka.auth_ws()
trenv = ka.getTREnv()

os_data = ["RBAQNVDA", "DNASNVDA"]

# 웹소켓 선언
kws = ka.KISWebSocket(api_url="/tryitout")

##############################################################################################
# [해외주식] 실시간시세 > 해외주식 실시간호가[실시간-021]
##############################################################################################

kws.subscribe(request=os_asking_price, data=os_data)

##############################################################################################
# [해외주식] 실시간시세 > 해외주식 실시간체결통보[실시간-009]
##############################################################################################

# kws.subscribe(request=os_ccnl_notice, data=os_data, kwargs={"env_dv": "real"})

##############################################################################################
# [해외주식] 실시간시세 > 해외주식 지연호가(아시아)[실시간-008]
##############################################################################################

# kws.subscribe(request=os_delayed_asking_price_asia, data=os_data)

##############################################################################################
# [해외주식] 실시간시세 > 해외주식 실시간지연체결가[실시간-007]
##############################################################################################

kws.subscribe(request=os_delayed_ccnl, data=os_data)


# 시작      / kis_auth : line 707
# def on_result(ws, tr_id, result, data_info):
#     print(result)# 이 함수 설정, llm코드의 같은 함수 참고
## 1000개 데이터 임시 저장 후 한번에 파일에 저장
import os
import pandas as pd
from datetime import datetime
from collections import defaultdict

SAVE_DIR = "realtime_data"
os.makedirs(SAVE_DIR, exist_ok=True)

buffers = defaultdict(list)     # 존재하지 않는 키에 접근할 때 오류가 아닌 미리 설정한 "list"를 자동 생성, 반환한다.
current_minute = defaultdict(lambda: None)

OVERFLOW_THRESHOLD = 1000

### overflow 제거, code 추가
def flush_to_parquet(key, minute_key, buffer_m=None):

    if len(buffers[key]) == 0 or len(key) == 1:
        print(key)
        return

    df = pd.concat(buffers[key], ignore_index=True)
    

    file_path = os.path.join(
        SAVE_DIR,
        key[0],
        key[1],
        f"{minute_key}.parquet"
    )

    # append 방식으로 저장
    if os.path.exists(file_path):       # ram 용량 임계점에 도달해서 분 변경x, 저장하려 할 때
        df.to_parquet(
            file_path,
            engine="pyarrow",
            compression="snappy",
            append=True
        )
    else:
        df.to_parquet(
            file_path,
            engine="pyarrow",       # 아래 터미널에 뜨는게 실시간으로 데이터 들어오는 모습
            compression="snappy"
        )
    if buffer_m is not None:
        file_path = os.path.join(
            SAVE_DIR,
            key[0],
            key[1],
            f"{minute_key}_snapshot.parquet"
        ) 
        buffer_m.to_parquet(
            file_path,
            engine="pyarrow",
            compression="snappy"
        )
    buffers[key].clear()


def on_result(ws, tr_id, code, result, data_info):      # 시간에 따라 저장 데이터가 다르므로 데이터 저장 분기를 여기서 작성
    if result.empty:
        return

    key = (code, tr_id)

    minute_key = datetime.now().strftime("%Y%m%d_%H%M")


    # 숫자형 변환
    for col in result.columns[1:]:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    if tr_id == "HDFSCNT0":             # 해외_실시간지연 체결가
        col_s = result.columns[[1, 6, 7, 11, 19, 20, 21, 22, 23, 24]]
        col_m = result.columns[[8, 9, 10, 13, 14]]
    else:                               # 해외_실시간 호가  / HDFSASP0
        col_s = result.columns[[1, 5, 6]].tolist() + result.columns[11:].tolist()
        col_m = result.columns[[7, 8, 9, 10]]


    #### 1데이터마다 한번 on_result 호출
    # 초기 minute 설정
    if current_minute[key] is None:
        current_minute[key] = minute_key
    # a분 에서 a+1분이 되면 새로운 디렉토리에 저장
    # 그게 아니라 용량이 임계점에 다다르면 기존 파일에 저장 후 시간은 새로고침 x
    
    ######### 여기서 한 번만 수집하는 데이터 저장

    # 1️⃣ minute 변경 시 flush (정상 저장)
    if minute_key != current_minute[key]:
        buffer_m = result[col_m]
        flush_to_parquet(       # 이게 db에 저장하는 함수, 위에 정의돼있음
            key,
            current_minute[key],
            buffer_m = buffer_m
        )
        current_minute[key] = minute_key

    # 버퍼 추가
    buffers[key].append(result[col_s])      # 버퍼는 db 저장 전 임시 저장공간

    # 2️⃣ 용량 초과 시 즉시 flush (메모리 보호)
    if len(buffers[key]) >= OVERFLOW_THRESHOLD:
        flush_to_parquet(
            key,
            minute_key,
        )


kws.start(on_result=on_result)
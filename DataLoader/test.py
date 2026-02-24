from datetime import datetime
import pandas as pd

input = "0|H0STASP0|001|000660^152522^A^959000^960000^961000^0^0^0^0^0^0^0^958000^957000^956000^0^0^0^0^0^0^0^3893^7010^4960^0^0^0^0^0^0^0^12^76^51^0^0^0^0^0^0^0^15863^139^0^0^959000^259810^259810^10000^2^1.05^3184369^0^0^0^0^0^0^0^0"
data = input.split('|')[3]
print(type(data[:6]))

now = datetime.now()
print(now.strftime("%H:%M:%S"))

columns = [
        "MKSC_SHRN_ISCD", "BSOP_HOUR", "HOUR_CLS_CODE",
        "ASKP1", "ASKP2", "ASKP3", "ASKP4", "ASKP5",
        "ASKP6", "ASKP7", "ASKP8", "ASKP9", "ASKP10",
        "BIDP1", "BIDP2", "BIDP3", "BIDP4", "BIDP5",
        "BIDP6", "BIDP7", "BIDP8", "BIDP9", "BIDP10",
        "ASKP_RSQN1", "ASKP_RSQN2", "ASKP_RSQN3", "ASKP_RSQN4", "ASKP_RSQN5",
        "ASKP_RSQN6", "ASKP_RSQN7", "ASKP_RSQN8", "ASKP_RSQN9", "ASKP_RSQN10",
        "BIDP_RSQN1", "BIDP_RSQN2", "BIDP_RSQN3", "BIDP_RSQN4", "BIDP_RSQN5",
        "BIDP_RSQN6", "BIDP_RSQN7", "BIDP_RSQN8", "BIDP_RSQN9", "BIDP_RSQN10",
        "TOTAL_ASKP_RSQN", "TOTAL_BIDP_RSQN", "OVTM_TOTAL_ASKP_RSQN", "OVTM_TOTAL_BIDP_RSQN",
        "ANTC_CNPR", "ANTC_CNQN", "ANTC_VOL", "ANTC_CNTG_VRSS", "ANTC_CNTG_VRSS_SIGN",
        "ANTC_CNTG_PRDY_CTRT", "ACML_VOL",
        "dummy1", "dummmy2", "dummy3", "dummy4", "dummy5", "dummy6", "dummy7", "dummy8"
]   # 59개
from io import StringIO
if input[0] in ["0", "1"]:
    d1 = input.split("|")
    if len(d1) < 4:
        raise ValueError("data not found...")

    tr_id = d1[1]            
  
    d = d1[3]

    code = d[:6]        # 종목 코드 저장
    df = pd.read_csv(       # 배치 단위로 들어오는 데이터 처리 가능
        StringIO(d), header=None, sep="^", names=columns, dtype=object
        )
    show_result = True
r = d.split("^")
print(len(r))
print(df)
print(len(columns))
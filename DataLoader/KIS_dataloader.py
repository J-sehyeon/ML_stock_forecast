import pandas as pd

#df = pd.read_parquet("realtime_data/000660/H0STASP0/20260225_1241.parquet")
#df = pd.read_parquet("realtime_data/NVDA/HDFSCNT0/20260303_0819.parquet")
df = pd.read_parquet("realtime_data/H0STASP0/20260304_0919.parquet")

print(df.head(20))
import os
os.path.exists()

# Excel 저장
df.to_excel("output_실시간호가.xlsx", index=False)


# 20260305_1315_snapshot.csv, 20260305_1436.csv
import os
import pandas as pd
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq
import glob


DATA = []

DATA_DIR = ""
SAVE_DIR = ""


def min2day(tr_key, tr_id, ymd):
    file_path = os.path.join(DATA_DIR, f"{tr_key}/{tr_id}/{ymd}.parquet")
    save_path = os.path.join(SAVE_DIR, f"{tr_key}/{tr_id}")
    csv_files = glob.glob(f"{file_path}/{ymd}_*.csv")

    tables = []

    for f in csv_files:
        table = pv.read_csv(f)
        tables.append(table)
    
    combined = pa.concat_tables(tables)

    pq.write_table(
        combined,
        save_path
    )
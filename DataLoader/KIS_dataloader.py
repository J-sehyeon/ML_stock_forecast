import pandas as pd

#df = pd.read_parquet("realtime_data/000660/H0STASP0/20260225_1241.parquet")
#df = pd.read_parquet("realtime_data/NVDA/HDFSCNT0/20260303_0819.parquet")
df = pd.read_parquet("realtime_data/H0STASP0/20260304_0919.parquet")

print(df.head(20))

# Excel 저장
df.to_excel("output_실시간호가.xlsx", index=False)

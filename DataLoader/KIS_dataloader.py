import pandas as pd

df = pd.read_parquet("realtime_data/H0STASP0_20260223_1520.parquet")

print(df.head(20))

# Excel 저장
# df.to_excel("output.xlsx", index=False)

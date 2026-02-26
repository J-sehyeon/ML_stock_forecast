import pandas as pd

df = pd.read_parquet("realtime_data/000660/H0STASP0/20260226_1238.parquet")

print(df.head(20))

# Excel 저장
df.to_excel("output_3.xlsx", index=False)

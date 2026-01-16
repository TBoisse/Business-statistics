import pandas as pd
from plotting import compute_profit_turnover

df = pd.read_csv("statistics.csv", sep=";")
start_date = "2025-01-10"
end_date = "2026-01-11"

print(compute_profit_turnover(df, start_date, end_date))


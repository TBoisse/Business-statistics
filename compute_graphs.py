import pandas as pd
from plotting import compute_profit_turnover

df = pd.read_csv("statistics.csv", sep=";")
start_date = "2025-01-01"
end_date = "2026-01-02"

print(compute_profit_turnover(df, start_date, end_date))


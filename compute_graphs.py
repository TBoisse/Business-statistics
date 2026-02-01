import pandas as pd
from plotting import compute_profit_turnover

df = pd.read_csv("statistics.csv", sep=";")
start_date = "2025-01-10"
end_date = "2026-03-01"

print("turnover, buy, turnover - buy")
print(compute_profit_turnover(df, start_date, end_date))


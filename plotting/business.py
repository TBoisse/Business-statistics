def compute_profit_turnover(df, start_date, end_date):
    df_turnover = df[df["type"] == "sell"]
    df_buy = df[df["type"] == "buy"]
    df_turnover_period = df_turnover[(df_turnover["date"] >= start_date) & (df_turnover["date"] <= end_date)]
    df_buy_period = df_buy[(df_buy["date"] >= start_date) & (df_buy["date"] <= end_date)]

    turnover = df_turnover_period["price"].sum()
    buy = df_buy_period["price"].sum()
    return turnover, buy, turnover - buy
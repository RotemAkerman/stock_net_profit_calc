# Description
Stock net profit calculator

Considers USD to any current currency and stock price (yfinance)
Considers 25% tax and possible [+3% tax](https://protocol.co.il/high-income-tax/)

# Usage
```
from datetime import datetime
from stock_net_profit_calc import StockPlan, calc_profit

plan = StockPlan(symbol='S',
                 start_date=datetime(2018, 2, 25),
                 exercise_price=3.4,
                 number_of_shares=5000,
                 vest_from_first_month=False)

print(calc_profit(stock_plans=[plan], local_currency='EUR'))
```
See quickstar.py for a few more options

from datetime import datetime
from stock_net_profit_calc import StockPlan, get_current_price, calc_profit

plan_a = StockPlan(symbol='S', start_date=datetime(2018, 2, 25), exercise_price=3.4, number_of_shares=5000,
                   vest_from_first_month=False)
plan_b = StockPlan(symbol='S', start_date=datetime(2019, 12, 14), exercise_price=7.1, number_of_shares=1000,
                   vest_from_first_month=True)

print(f'S current price is: {get_current_price("S")}$')

print(calc_profit([plan_a, plan_b]))  # Will calc by current stock price

print(calc_profit([plan_a, plan_b], by_price=100))

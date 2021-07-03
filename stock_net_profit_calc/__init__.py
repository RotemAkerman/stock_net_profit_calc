# -*- coding: utf-8 -*-
import datetime

import yfinance as yf
from currency_converter import CurrencyConverter


def usd_to_ils(num):
    c = CurrencyConverter()
    return c.convert(num, 'USD', 'ILS')


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'][0],2)
    # return ticker.info['regularMarketPrice']


def get_vested_months_count(start_date, vest_from_first):
    end_date = datetime.datetime.now()
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if end_date.day < start_date.day:
        num_months -= 1
    if num_months < 12 and not vest_from_first:
        return 0
    elif num_months > 48:
        return 48
    return num_months


def calc_profit(stock_plans, by_price=None):
    output = ''
    total_vested = 0
    total = 0
    for i, stock_plan in enumerate(stock_plans):
        stock_price = by_price or get_current_price(stock_plan.symbol)
        pps = (stock_price - stock_plan.exercise_price)
        number_of_vested_shares = stock_plan.number_of_shares / 48 * get_vested_months_count(stock_plan.start_date,
                                                                                             stock_plan.vest_from_first_month)

        profit_before_tax_usd = pps * stock_plan.number_of_shares
        profit_before_tax_ils = usd_to_ils(profit_before_tax_usd)
        tax = 0.72 if profit_before_tax_ils > 647640 else 0.75
        profit_after_tax_ils = round(profit_before_tax_ils * tax, 2)
        total += profit_before_tax_ils * tax

        vested_profit_before_tax_usd = pps * number_of_vested_shares
        vested_profit_before_tax_ils = usd_to_ils(vested_profit_before_tax_usd)
        vested_profit_after_tax_ils = round(vested_profit_before_tax_ils * tax, 2)
        total_vested += vested_profit_before_tax_ils * tax

        output += f'Plan {i+1} ({stock_plan.symbol}): ' \
                  f'Vested {vested_profit_after_tax_ils:,}₪ (After fully vested: {profit_after_tax_ils:,}₪)\n'
    output += f'Total vested: {round(total_vested,2):,}₪\n'
    output += f'Total after fully vested: {round(total, 2):,}₪'
    return output


class StockPlan(object):
    def __init__(self, symbol, start_date, exercise_price, number_of_shares, vest_from_first_month=False):
        self.symbol = symbol
        self.start_date = start_date
        self.exercise_price = exercise_price
        self.number_of_shares = number_of_shares
        self.vest_from_first_month = vest_from_first_month  # False = vest from 13th month + retro, else from 1st month

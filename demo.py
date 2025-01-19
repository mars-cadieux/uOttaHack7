#$START$
import requests
import json
import yfinance as yf
import pandas as pd
import yahoo_fin.stock_info as si
import yahoo_fin.options as ops
#$END$

def get_current_stock_info(ticker):
    """
    This function takes a stock ticker as input and returns current stock information.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    dict: A dictionary containing current stock information.
    """
    stock_info = si.get_quote_table(ticker)
    return stock_info

def get_historical_data(ticker, start_date, end_date, interval):
    """
    This function takes a stock ticker, start date, end date, and interval as input and returns historical data.

    Parameters:
    ticker (str): The stock ticker symbol.
    start_date (str): The start date for historical data.
    end_date (str): The end date for historical data.
    interval (str): The interval for historical data (e.g., 1d, 1wk, 1mo).

    Returns:
    pandas.DataFrame: A pandas DataFrame containing historical data.
    """
    historical_data = si.get_data(ticker, start_date=start_date, end_date=end_date, interval=interval)
    return historical_data

def get_fundamental_data(ticker):
    """
    This function takes a stock ticker as input and returns fundamental data.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: A pandas DataFrame containing fundamental data.
    """
    fundamental_data = si.get_stats_valuation(ticker)
    return fundamental_data

def get_income_statement(ticker):
    """
    This function takes a stock ticker as input and returns income statement data.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: A pandas DataFrame containing income statement data.
    """
    income_statement = si.get_income_statement(ticker)
    return income_statement

def get_balance_sheet(ticker):
    """
    This function takes a stock ticker as input and returns balance sheet data.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: A pandas DataFrame containing balance sheet data.
    """
    balance_sheet = si.get_balance_sheet(ticker)
    return balance_sheet

def get_cash_flow_statement(ticker):
    """
    This function takes a stock ticker as input and returns cash flow statement data.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: A pandas DataFrame containing cash flow statement data.
    """
    cash_flow_statement = si.get_cash_flow(ticker)
    return cash_flow_statement

def get_options_data(ticker):
    """
    This function takes a stock ticker as input and returns options data.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    list: A list of expiration dates for options data.
    """
    expiration_dates = ops.get_expiration_dates(ticker)
    return expiration_dates

print(get_current_stock_info('APPL'))
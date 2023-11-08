import pandas as pd

from ..courtois.fmp_url import get_data_url

from datetime import datetime
from dateutil.relativedelta import relativedelta

def company_profile(apikey: str='apikey', symbol: str='AAPL'):
    """
    params:
        apikey -- to access data from FMP;
        symbol -- ticker of company;
    return: list of dictionaries
    """
    url = (f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={apikey}')
    data = get_data_url(url=url)
    return data

def get_fs_some(apikey: str='apikey', symbol: str='AAPL', period: str='annual',
                limit: int=10, finance: str='balance-sheet-statement'):
    """
    params:
        apikey -- to access data from FMP;
        symbol -- ticker of company;
        period -- either 'annual' or 'quarter';
        limit -- number of data points;
        finance -- can be 'balance-sheet-statement', or 'income-statement', or 'cash-flow-statement', or 'enterprise-values', 
            or 'ratios'
    return: list of dictionaries
    """
    url = (f'https://financialmodelingprep.com/api/v3/{finance}/{symbol}?period={period}&limit={limit}&apikey={apikey}')
    data = get_data_url(url=url)
    return data

def get_employees_number(apikey: str='apikey', symbol: str='AAPL'):
    """
    params:
        apikey -- to access data from FMP;
        symbol -- ticker of company;
    return: list of dictionaries
    """

    url = (f"https://financialmodelingprep.com/api/v4/historical/employee_count?symbol={symbol}&apikey={apikey}")
    data = get_data_url(url=url)
    return data
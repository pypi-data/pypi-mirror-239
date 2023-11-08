import pandas as pd

from .get_info import get_employees_number



def get_employees_counts(apikey: str='apikey', ticks: list=['AAPL', 'MSFT'], period: str = 'annual', 
           with_progress: bool = False):
    
    """
    params:
        apikey -- to access data from FMP;
        ticks -- list of tickers;
        period -- either 'annual' or 'quarter';
        with_progress -- if you want to visualize progress;
    return: data frame of employees number
    """
    
    if with_progress:
        n = len(ticks)
        i=0

    employees = []

    for ticker in ticks:
        try:
            ticker_data = get_employees_number(apikey=apikey, symbol=ticker)
            employees.append(pd.DataFrame(ticker_data))
            if with_progress:
                i += 1
                print(f"For {ticker}: {i} / {n}")
        except:
            pass

    employees_df = pd.concat(employees, axis=0)

    return employees_df
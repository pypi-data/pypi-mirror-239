from ..courtois.fmp_url import get_data_url

def earning_transcript(apikey: str='apikey', symbol: str='AAPL', year: int=2020, quarter: int=4):
    """
    params:
        apikey -- to access data from FMP;
        symbol -- ticker of company;
    return: list of dictionaries
    """
    
    url = (f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{symbol}?year={year}&quarter={quarter}&apikey={apikey}")

    data = get_data_url(url=url)

    return data

def general_news(apikey: str='apikey', page: int=1):
    """
    params:
        apikey -- to access data from FMP;
        page -- page;
    return: list of dictionaries
    """
    
    url = (f"https://financialmodelingprep.com/api/v4/general_news?page={page}&apikey={apikey}")

    data = get_data_url(url=url)

    return data

def fmp_articles(apikey: str='apikey', page: int=1, size: int=5):
    """
    params:
        apikey -- to access data from FMP;
        page -- page;
        size -- number of items in the page
    return: list of dictionaries
    """
    
    url = (f"https://financialmodelingprep.com/api/v3/fmp/articles?page={page}&size={size}&apikey={apikey}")

    data = get_data_url(url=url)

    return data

def stock_news(apikey: str='apikey', page: int=1):
    """
    params:
        apikey -- to access data from FMP;
        page -- page;
    return: list of dictionaries
    """
    
    url = (f"https://financialmodelingprep.com/api/v3/stock_news?page={page}&apikey={apikey}")

    data = get_data_url(url=url)

    return data

def sentiments(apikey: str='apikey', page: int=1):
    """
    params:
        apikey -- to access data from FMP;
        page -- page;
    return: list of dictionaries
    """
    
    url = (f"https://financialmodelingprep.com/api/v4/stock-news-sentiments-rss-feed?page={page}&apikey={apikey}")

    data = get_data_url(url=url)

    return data

def press_releases(apikey: str='apikey', symbol: str='AAPL'):
    """
    params:
        apikey -- to access data from FMP;
        page -- page;
    return: list of dictionaries
    """
    
    url = (f"https://financialmodelingprep.com/api/v3/press-releases/{symbol}?apikey={apikey}")

    data = get_data_url(url=url)

    return data




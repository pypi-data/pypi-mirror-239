import pandas as pd

# from ..courtois.fmp_url import get_data_url
from .get_info import company_profile, get_fs_some

from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_years(start_date: str):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    now = datetime.now()
    difference = relativedelta(start_datetime, now)
    years = abs(difference.years)
    return years

def calculate_months(start_date: str):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    now = datetime.now()
    difference = relativedelta(start_datetime, now)
    months = abs(difference.months) + abs(12*difference.years)
    return months

def get_fs(apikey: str='apikey', ticks: list=['AAPL', 'MSFT'], period: str = 'annual', 
           with_progress: bool = False, include_sic: bool = False, 
           bs_m=None, is_m=None, cf_m=None, ev_m=None, start_date: str= "N/A"):
    """
    params:
        apikey -- to access data from FMP;
        ticks -- list of tickers;
        period -- either 'annual' or 'quarter';
        with_progress -- if you want to visualize progress;
        include_sic -- if you want also extract sector and industry information
        bs_m -- the information from balance sheet like 'inventory', 'totalAssets', 'accountPayables' and so on...
                on default extracts maximum information from balance sheet
        is_m -- the information from balance sheet like 'revenue', 'grossProfit', 'eps', and so on...
                on default extracts maximum information from income statement
        cf_m -- the information from balance sheet like 'capitalExpenditure', 'dividendsPaid', 'operatingCashFlow' and so on...
                on default extracts maximum information from cash flow statement
        ev_m -- the information from balance sheet like 'enterpriseValue', 'marketCapitalization', 'numberOfShares', and 'stockPrice'
        start_date -- from which date we want to get financial statements
    return: data frame of financial statements
    """
    
    if start_date == "N/A":
        limit = 100;
    else:
        if period == "annual":
            limit = calculate_years(start_date=start_date) + 1;
        elif period == "quarter":
            limit = calculate_months(start_date=start_date) // 3 + 1;
        else:
            print("The period should be either 'annual' or 'quarter' ");
            return False;

    attributes = {
        'balance-sheet-statement': ['reportedCurrency', 'totalNonCurrentAssets', 'taxAssets', 'shortTermInvestments',
                         'longTermDebt', 'preferredStock', 'commonStock', 'totalLiabilitiesAndTotalEquity',
                         'deferredRevenue', 'goodwillAndIntangibleAssets', 'capitalLeaseObligations',
                         'totalStockholdersEquity', 'otherNonCurrentLiabilities', 'totalDebt', 'intangibleAssets',
                         'minorityInterest', 'otherAssets', 'propertyPlantEquipmentNet', 'cashAndShortTermInvestments',
                         'symbol', 'totalEquity', 'totalLiabilities', 'otherNonCurrentAssets', 'otherCurrentLiabilities',
                         'retainedEarnings', 'totalNonCurrentLiabilities', 'othertotalStockholdersEquity',
                         'deferredRevenueNonCurrent', 'accountPayables', 'totalCurrentLiabilities', 'totalCurrentAssets',
                         'longTermInvestments', 'deferredTaxLiabilitiesNonCurrent', 'netReceivables', 'taxPayables',
                         'shortTermDebt', 'cashAndCashEquivalents', 'inventory', 'otherCurrentAssets', 'netDebt', 'date',
                         'otherLiabilities', 'goodwill', 'totalInvestments', 'totalLiabilitiesAndStockholdersEquity',
                         'totalAssets', 'accumulatedOtherComprehensiveIncomeLoss'],
        'income-statement': ['incomeBeforeTaxRatio', 'incomeTaxExpense', 'totalOtherIncomeExpensesNet', 'revenue', 
                         'costOfRevenue', 'otherExpenses', 'netIncome', 'generalAndAdministrativeExpenses',
                         'ebitdaratio', 'eps', 'symbol', 'operatingIncomeRatio', 'sellingGeneralAndAdministrativeExpenses',
                         'weightedAverageShsOut', 'operatingExpenses', 'weightedAverageShsOutDil', 'interestExpense',
                         'incomeBeforeTax', 'epsdiluted', 'depreciationAndAmortization', 'ebitda',
                         'sellingAndMarketingExpenses', 'date', 'grossProfit', 'costAndExpenses', 'grossProfitRatio',
                         'researchAndDevelopmentExpenses', 'netIncomeRatio', 'interestIncome', 'operatingIncome'],
        'cash-flow-statement': ['otherWorkingCapital', 'commonStockRepurchased', 'investmentsInPropertyPlantAndEquipment',
                         'dividendsPaid', 'otherNonCashItems', 'netCashUsedForInvestingActivites', 'freeCashFlow',
                         'cashAtEndOfPeriod', 'commonStockIssued', 'effectOfForexChangesOnCash', 'symbol',
                         'otherFinancingActivites', 'netCashProvidedByOperatingActivities',
                         'netCashUsedProvidedByFinancingActivities', 'deferredIncomeTax', 'stockBasedCompensation',
                         'changeInWorkingCapital', 'netChangeInCash', 'debtRepayment', 'acquisitionsNet', 'accountsPayables',
                         'operatingCashFlow', 'date', 'accountsReceivables', 'salesMaturitiesOfInvestments',
                         'cashAtBeginningOfPeriod', 'otherInvestingActivites', 'purchasesOfInvestments', 'capitalExpenditure'],
        'enterprise-values': ['enterpriseValue', 'marketCapitalization', 'numberOfShares', 'stockPrice', 'date', 'symbol']
    }
    
    metrics = {'balance-sheet-statement': bs_m, 'income-statement': is_m,
               'cash-flow-statement': cf_m, 'enterprise-values': ev_m}
    fss = ['balance-sheet-statement', 'income-statement', 'cash-flow-statement', 'enterprise-values']
    attributes_fss = {}

    for fs in fss:
        if (metrics[fs] == None):
            attributes_fs = attributes[fs]
        elif (metrics[fs] == []):
            attributes_fs = []
        else:
            attributes_fs = set(metrics[fs]);
            attributes_fs.add('date');
            attributes_fs.add('symbol');
            attributes_fs = list(attributes_fs);
    
        attributes_fss[fs] = attributes_fs

    data_frames = []

    if with_progress:
        i = 0;
        n = len(ticks);

    fss = ['balance-sheet-statement', 'income-statement', 'cash-flow-statement', 'enterprise-values']

    for ticker in ticks:

        inventory_frames = []

        if with_progress:
            i += 1;
        
        for fs in fss:

            if (attributes_fss[fs] == []):
                continue;
            else:
                ticker_data = get_fs_some(apikey=apikey, symbol=ticker, period=period, limit=limit, finance=fs)

                try:
                    data_df = pd.DataFrame(ticker_data)
                    data_df = data_df[list(set(attributes_fss[fs]).intersection(set(data_df.columns)))]
                    data_df.drop_duplicates(subset=['symbol', 'date'], inplace=True)
                    data_df.set_index(['symbol', 'date'], inplace=True)
                    inventory_frames.append(data_df)
                except:
                    pass

        if (inventory_frames == []):
            continue;
        else:
            try:
                data_inventory_stock_q = pd.concat(inventory_frames, axis=1)
                data_frames.append(data_inventory_stock_q)

                if with_progress:
                    print(f"With ticker (fs) -- {ticker} : {str(i)} / {str(n)} with limit -- {str(limit)} ")
            except:
                continue
    
    # print(data_frames)

    if start_date == "N/A":
        df = pd.concat(data_frames)
    else:
        df = pd.concat(data_frames)
        df.reset_index(inplace=True)

        df = df[df['date'] >= start_date]

        df.set_index(['symbol', 'date'], inplace=True)

    if include_sic:
        tickers_downloaded = list(set(df.index.get_level_values(0)))

        df.reset_index(inplace=True)

        df['sector'] = 'other';
        df['industry'] = 'other';

        if with_progress:
            i = 0;
            n = len(tickers_downloaded);

        for ticker in tickers_downloaded:
            if with_progress:
                i += 1;

            profile = company_profile(apikey=apikey, symbol=ticker);

            if profile != []:
                df.loc[df['symbol'] == ticker, 'sector'] = profile[0].get('sector', 'other');
                df.loc[df['symbol'] == ticker, 'industry'] = profile[0].get('industry', 'other');
                if with_progress:
                    print(f"For ticker (sic) -- {ticker} : {str(i)} / {str(n)}");

        df.set_index(['symbol', 'date'], inplace=True)

    return df
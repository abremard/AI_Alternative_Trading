""" Preprocessor for technical analysis
"""

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

import pandas as pd

from elk import search

def parse_bs(elastic_docs):
    """ Parse balance sheet data to dataframe

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index

    Returns:
        Dataframe.Object: parsed document
    """    
    
    documents = []
    docs = pd.DataFrame()
    
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # append the Series object to the DataFrame object
        doc_data = pd.Series(source_data, name=source_data['fiscalDateEnding'])
        docs = docs.append(doc_data)
    
    docs.totalAssets = pd.to_numeric(docs.totalAssets, errors='coerce').astype(float)
    docs.totalCurrentAssets = pd.to_numeric(docs.totalCurrentAssets, errors='coerce').astype(float)
    docs.cashAndCashEquivalentsAtCarryingValue = pd.to_numeric(docs.cashAndCashEquivalentsAtCarryingValue, errors='coerce').astype(float)
    docs.cashAndShortTermInvestments = pd.to_numeric(docs.cashAndShortTermInvestments, errors='coerce').astype(float)
    docs.inventory = pd.to_numeric(docs.inventory, errors='coerce').astype(float)
    docs.currentNetReceivables = pd.to_numeric(docs.currentNetReceivables, errors='coerce').astype(float)
    docs.totalNonCurrentAssets = pd.to_numeric(docs.totalNonCurrentAssets, errors='coerce').astype(float)
    docs.propertyPlantEquipment = pd.to_numeric(docs.propertyPlantEquipment, errors='coerce').astype(float)
    docs.accumulatedDepreciationAmortizationPPE = pd.to_numeric(docs.accumulatedDepreciationAmortizationPPE, errors='coerce').astype(float)
    docs.intangibleAssets = pd.to_numeric(docs.intangibleAssets, errors='coerce').astype(float)
    docs.intangibleAssetsExcludingGoodwill = pd.to_numeric(docs.intangibleAssetsExcludingGoodwill, errors='coerce').astype(float)
    docs.goodwill = pd.to_numeric(docs.goodwill, errors='coerce').astype(float)
    docs.investments = pd.to_numeric(docs.investments, errors='coerce').astype(float)
    docs.longTermInvestments = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.shortTermInvestments = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.otherCurrentAssets = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.otherNonCurrrentAssets = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.totalLiabilities = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.totalCurrentLiabilities = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.currentAccountsPayable = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.deferredRevenue = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.currentDebt = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.shortTermDebt = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.totalNonCurrentLiabilities = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.capitalLeaseObligations = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.longTermDebt = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.currentLongTermDebt = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.longTermDebtNoncurrent = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.shortLongTermDebtTotal = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.otherCurrentLiabilities = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.otherNonCurrentLiabilities = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.totalShareholderEquity = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.treasuryStock = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.retainedEarnings = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.commonStock = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    docs.commonStockSharesOutstanding = pd.to_numeric(docs.longTermInvestments, errors='coerce').astype(float)
    
    return docs

def parse_cf(elastic_docs):
    """ Parse cash flow data to dataframe

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index

    Returns:
        Dataframe.Object: parsed document
    """    
    
    documents = []
    docs = pd.DataFrame()
    
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # append the Series object to the DataFrame object
        doc_data = pd.Series(source_data, name=source_data['fiscalDateEnding'])
        docs = docs.append(doc_data)
    
    docs.operatingCashflow = pd.to_numeric(docs.operatingCashflow, errors='coerce').astype(float)
    docs.paymentsForOperatingActivities = pd.to_numeric(docs.paymentsForOperatingActivities, errors='coerce').astype(float)
    docs.proceedsFromOperatingActivities = pd.to_numeric(docs.proceedsFromOperatingActivities, errors='coerce').astype(float)
    docs.changeInOperatingLiabilities = pd.to_numeric(docs.changeInOperatingLiabilities, errors='coerce').astype(float)
    docs.changeInOperatingAssets = pd.to_numeric(docs.changeInOperatingAssets, errors='coerce').astype(float)
    docs.depreciationDepletionAndAmortization = pd.to_numeric(docs.depreciationDepletionAndAmortization, errors='coerce').astype(float)
    docs.capitalExpenditures = pd.to_numeric(docs.capitalExpenditures, errors='coerce').astype(float)
    docs.changeInReceivables = pd.to_numeric(docs.changeInReceivables, errors='coerce').astype(float)
    docs.changeInInventory = pd.to_numeric(docs.changeInInventory, errors='coerce').astype(float)
    docs.profitLoss = pd.to_numeric(docs.profitLoss, errors='coerce').astype(float)
    docs.cashflowFromInvestment = pd.to_numeric(docs.cashflowFromInvestment, errors='coerce').astype(float)
    docs.cashflowFromFinancing = pd.to_numeric(docs.cashflowFromFinancing, errors='coerce').astype(float)
    docs.proceedsFromRepaymentsOfShortTermDebt = pd.to_numeric(docs.proceedsFromRepaymentsOfShortTermDebt, errors='coerce').astype(float)
    docs.paymentsForRepurchaseOfCommonStock = pd.to_numeric(docs.paymentsForRepurchaseOfCommonStock, errors='coerce').astype(float)
    docs.paymentsForRepurchaseOfEquity = pd.to_numeric(docs.paymentsForRepurchaseOfEquity, errors='coerce').astype(float)
    docs.paymentsForRepurchaseOfPreferredStock = pd.to_numeric(docs.paymentsForRepurchaseOfPreferredStock, errors='coerce').astype(float)
    docs.dividendPayout = pd.to_numeric(docs.dividendPayout, errors='coerce').astype(float)
    docs.dividendPayoutCommonStock = pd.to_numeric(docs.dividendPayoutCommonStock, errors='coerce').astype(float)
    docs.dividendPayoutPreferredStock = pd.to_numeric(docs.dividendPayoutPreferredStock, errors='coerce').astype(float)
    docs.proceedsFromIssuanceOfCommonStock = pd.to_numeric(docs.proceedsFromIssuanceOfCommonStock, errors='coerce').astype(float)
    docs.proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = pd.to_numeric(docs.proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet, errors='coerce').astype(float)
    docs.proceedsFromIssuanceOfPreferredStock = pd.to_numeric(docs.proceedsFromIssuanceOfPreferredStock, errors='coerce').astype(float)
    docs.proceedsFromRepurchaseOfEquity = pd.to_numeric(docs.proceedsFromRepurchaseOfEquity, errors='coerce').astype(float)
    docs.proceedsFromSaleOfTreasuryStock = pd.to_numeric(docs.proceedsFromSaleOfTreasuryStock, errors='coerce').astype(float)
    docs.changeInCashAndCashEquivalents = pd.to_numeric(docs.changeInCashAndCashEquivalents, errors='coerce').astype(float)
    docs.changeInExchangeRate = pd.to_numeric(docs.changeInExchangeRate, errors='coerce').astype(float)
    docs.netIncome = pd.to_numeric(docs.netIncome, errors='coerce').astype(float)
    
    return docs

def parse_e(elastic_docs):
    """ Parse earnings data to dataframe

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index

    Returns:
        Dataframe.Object: parsed document
    """    
    
    documents = []
    docs = pd.DataFrame()
    
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # append the Series object to the DataFrame object
        doc_data = pd.Series(source_data, name=source_data['fiscalDateEnding'])
        docs = docs.append(doc_data)
    
    docs.reportedEPS = pd.to_numeric(docs.reportedEPS, errors='coerce').astype(float)
    docs.estimatedEPS = pd.to_numeric(docs.estimatedEPS, errors='coerce').astype(float)
    docs.surprise = pd.to_numeric(docs.surprise, errors='coerce').astype(float)
    docs.surprisePercentage = pd.to_numeric(docs.surprisePercentage, errors='coerce').astype(float)
    
    return docs

def parse_is(elastic_docs):
    """ Parse income statement to dataframe

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index

    Returns:
        Dataframe.Object: parsed document
    """    
    
    documents = []
    docs = pd.DataFrame()
    
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # append the Series object to the DataFrame object
        doc_data = pd.Series(source_data, name=source_data['fiscalDateEnding'])
        docs = docs.append(doc_data)
    
    docs.grossProfit = pd.to_numeric(docs.grossProfit, errors='coerce').astype(float)
    docs.totalRevenue = pd.to_numeric(docs.totalRevenue, errors='coerce').astype(float)
    docs.costOfRevenue = pd.to_numeric(docs.costOfRevenue, errors='coerce').astype(float)
    docs.costofGoodsAndServicesSold = pd.to_numeric(docs.costofGoodsAndServicesSold, errors='coerce').astype(float)
    docs.operatingIncome = pd.to_numeric(docs.operatingIncome, errors='coerce').astype(float)
    docs.sellingGeneralAndAdministrative = pd.to_numeric(docs.sellingGeneralAndAdministrative, errors='coerce').astype(float)
    docs.researchAndDevelopment = pd.to_numeric(docs.researchAndDevelopment, errors='coerce').astype(float)
    docs.operatingExpenses = pd.to_numeric(docs.operatingExpenses, errors='coerce').astype(float)
    docs.investmentIncomeNet = pd.to_numeric(docs.investmentIncomeNet, errors='coerce').astype(float)
    docs.netInterestIncome = pd.to_numeric(docs.netInterestIncome, errors='coerce').astype(float)
    docs.interestIncome = pd.to_numeric(docs.interestIncome, errors='coerce').astype(float)
    docs.interestExpense = pd.to_numeric(docs.interestExpense, errors='coerce').astype(float)
    docs.nonInterestIncome = pd.to_numeric(docs.nonInterestIncome, errors='coerce').astype(float)
    docs.otherNonOperatingIncome = pd.to_numeric(docs.otherNonOperatingIncome, errors='coerce').astype(float)
    docs.depreciation = pd.to_numeric(docs.depreciation, errors='coerce').astype(float)
    docs.depreciationAndAmortization = pd.to_numeric(docs.depreciationAndAmortization, errors='coerce').astype(float)
    docs.incomeBeforeTax = pd.to_numeric(docs.incomeBeforeTax, errors='coerce').astype(float)
    docs.incomeTaxExpense = pd.to_numeric(docs.incomeTaxExpense, errors='coerce').astype(float)
    docs.interestAndDebtExpense = pd.to_numeric(docs.interestAndDebtExpense, errors='coerce').astype(float)
    docs.netIncomeFromContinuingOperations = pd.to_numeric(docs.netIncomeFromContinuingOperations, errors='coerce').astype(float)
    docs.comprehensiveIncomeNetOfTax = pd.to_numeric(docs.comprehensiveIncomeNetOfTax, errors='coerce').astype(float)
    docs.ebit = pd.to_numeric(docs.ebit, errors='coerce').astype(float)
    docs.ebitda = pd.to_numeric(docs.ebitda, errors='coerce').astype(float)
    docs.netIncome = pd.to_numeric(docs.netIncome, errors='coerce').astype(float)
    
    return docs

def preprocess():
    """ Load data from elasticsearch, parse into dataframe and compute features
    """    
    # Load data from elastic search to dataframe
    balance_sheet = search.balance_sheet(symbols=['AAPL'], size=500)
    cash_flow = search.cash_flow(symbols=['AAPL'], size=500)
    earnings = search.earnings(symbols=['AAPL'], size=500)
    income_statement = search.income_statement(symbols=['AAPL'], size=500)

    # Parse data into dataframe
    bs_df = parse_bs(elastic_docs=balance_sheet)
    cf_df = parse_cf(elastic_docs=cash_flow)
    e_df = parse_e(elastic_docs=earnings)
    is_df = parse_is(elastic_docs=income_statement)
    
preprocess()
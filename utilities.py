import pandas as pd

def load_and_prepare_data():
    income_data = pd.read_csv('Data/us-income-quarterly.csv')
    balance_data = pd.read_csv('Data/us-balance-quarterly.csv')
    cashflow_data = pd.read_csv('Data/us-cashflow-quarterly.csv')

    # Mapping quarters
    quarter_mapping = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
    income_data['Fiscal Period'] = income_data['Fiscal Period'].map(quarter_mapping)
    balance_data['Fiscal Period'] = balance_data['Fiscal Period'].map(quarter_mapping)
    cashflow_data['Fiscal Period'] = cashflow_data['Fiscal Period'].map(quarter_mapping)

    # Sorting by fiscal year and period
    income_data.sort_values(by=['Fiscal Year', 'Fiscal Period'], inplace=True)
    balance_data.sort_values(by=['Fiscal Year', 'Fiscal Period'], inplace=True)
    cashflow_data.sort_values(by=['Fiscal Year', 'Fiscal Period'], inplace=True)

    return income_data, balance_data, cashflow_data

def get_financials_for_period(income_data, balance_data, cashflow_data, ticker, year, quarter):
    income = income_data.loc[(income_data['Ticker'] == ticker) & (income_data['Fiscal Year'] == year) & (income_data['Fiscal Period'] == quarter)]
    balance = balance_data.loc[(balance_data['Ticker'] == ticker) & (balance_data['Fiscal Year'] == year) & (balance_data['Fiscal Period'] == quarter)]
    cashflow = cashflow_data.loc[(cashflow_data['Ticker'] == ticker) & (cashflow_data['Fiscal Year'] == year) & (cashflow_data['Fiscal Period'] == quarter)]
    
    return income, balance, cashflow

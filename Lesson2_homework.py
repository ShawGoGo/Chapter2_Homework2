import pandas as pd
import numpy as np
import datetime as dt


### 1st Question
fund_df = pd.read_csv('fundamentals.csv')
print(fund_df.head())
print(fund_df.shape)
# 1.1 S&P500股票在2015年`net income`的均值是多少？
print(fund_df.columns)
fund_df['Period Ending'] = pd.to_datetime(fund_df['Period Ending'])
fund_df = fund_df.set_index('Period Ending')
fund_df_2015 = fund_df['2015']
net_2015_mean = fund_df_2015['Net Income'].mean()
print(net_2015_mean)
# 最大值比最小值多多少？
net_2015_dif = fund_df_2015['Net Income'].max()-fund_df_2015['Net Income'].min()
print(net_2015_dif)
# 1.2.1 S&P500股票在2016年的固定资产（fixed assets）占总资产(total assets)比例的均值是多少？

fund_df['ratio'] = fund_df[['Fixed Assets', 'Total Assets']].apply(
    lambda x: x['Fixed Assets'] / x['Total Assets'], axis=1)
fund_df_2016 = fund_df['2016']
ratio_2016_mean = fund_df_2016['ratio'].mean()
print(ratio_2016_mean)
# 1.2.2 固定资产占总资产比例最小的股票是的代码（ticker symbol）是什么？
ratio_min_ind = fund_df_2016['ratio'].idxmin()
ratio_min = fund_df_2016['ratio'].min()
min_Ticker_Symbol = fund_df_2016.loc[ratio_min_ind, 'Ticker Symbol']
min_Ticker_Symbol = fund_df_2016.loc[fund_df_2016.ratio == ratio_min, 'Ticker Symbol']


### 2nd Question
sec_df = pd.read_csv('securities.csv')
sec_df.head(10)
#2.1 请列举出各个sector中的加入时间最早的股票名称
sec_df['Date first added'] = pd.to_datetime(sec_df['Date first added'])
sector_earliest_ind = sec_df['Date first added'].idxmin()
sector_earliest = sec_df.loc[sector_earliest_ind]['GICS Sector']

#2.2. 请列举出每一个州中加入时间最晚的股票名称
state_latest_ind = sec_df.groupby('Address of Headquarters')['Date first added'].idxmax()

state_latest = sec_df.loc[state_latest_ind]['Ticker symbol']
state_latest_ind = pd.DataFrame(state_latest_ind)
state_latest_ind = state_latest_ind.reset_index()
state_latest = pd.DataFrame(state_latest)
state_latest = state_latest.reset_index()
state_latest.rename(columns={'index': 'Date first added'},inplace=True)
state_latest_df = pd.merge(state_latest_ind, state_latest, on='Date first added', how='left')
state_latest_df.to_csv('加入时间最晚的股票名称.csv')
state_latest_df.head(10)
#3.1. 请思考，合并两个表的信息的时候，我们应该用什么样的准则对其它们
#3.2. 请列举每个sector在2013-2016年累计Research&Development的总投入
start_date = '2013-01-01'
end_date = '2016-12-31'

mask = (sec_df['Date first added'] >= start_date) & (sec_df['Date first added'] <= end_date)
sec_df = sec_df.loc[mask]
sector_df_sum = sec_df.groupby('GICS Sector')['CIK'].sum()
sector_df_sum = pd.DataFrame(sector_df_sum)
sector_df_sum.to_csv('累计Research&Development的总投入.csv')

#3.3. 请列举出每个sector中，在2013-2016年累计Research&development投入最大的3家公司的名称以及投入的数值
sector_df_sum_sort = sector_df_sum.sort_values(ascending=False)
sector_df_sum_sort.head(3)
#4. 假设你是某基金公司的老板，现在对于每只股票，你都专门安排了一位负责它的交易员。公司规定每一位交易员手中的资金要么全部买入要么全部卖出（空仓，转化为现金）。假设2016年每一位交易员手中都有10000美元，假设他们都能够看到2016年全年的数据，假设他们都能抓住每一次机会，那么请问2016年底时，赚钱最多的股票是哪一只，赚了多少钱？"

price_df = pd.read_csv('prices.csv')
price_df.head(10)
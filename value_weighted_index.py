# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:28:35 2023

@author: DOR
"""


#------------------------------value-weighted index-----------------------

#-----------------------------------------Part 1--------------------------
import pandas as pd
import matplotlib.pyplot as plt

filename=r'C:\Daymler\daymler\DataCamp\Python\Time_Series'
 
listings=pd.concat(pd.read_excel(filename + "/"+ 'listings.xlsx', sheet_name=None,
                       na_values='n/a'), ignore_index=True)


# Inspect listings
print(listings.info())

# Move 'stock symbol' into the index
listings.set_index('Stock Symbol', inplace=True)

# Drop rows with missing 'sector' data
listings.dropna(subset=['Sector'], inplace=True)

# Select companies with IPO Year before 2019
listings = listings[listings['IPO Year']<2019]

# Inspect the new listings data
print(listings.info())

# Show the number of companies per sector
print(listings.groupby('Sector').size().sort_values(ascending=False))

#----------------------------------Part 2---------------------------------------

# Select largest company for each sector
components = listings.groupby('Sector')['Market Capitalization'].nlargest(1)

# Print components, sorted by market cap
print(components.sort_values(ascending=False))

# Select stock symbols and print the result
tickers = components.index.get_level_values(1)
print(tickers)

# Print company name, market cap, and last price for each component 
info_cols = ['Company Name', 'Market Capitalization', 'Last Sale']
print(listings.loc[tickers, info_cols].sort_values('Market Capitalization', ascending=False))


#-------------------------------------Part 3--------------------------------------


#Import prices and inspect result
stock_prices = pd.read_csv(filename +"/"+ 'stock_data.csv', parse_dates=['Date'], index_col='Date').dropna()
print(stock_prices.info())

# Calculate the returns for the index components
price_return = (stock_prices.iloc[-1]/stock_prices.iloc[0]-1)*100

# Plot horizontal bar chart of sorted price_return   

price_return.sort_values().plot(kind='barh', title='Stock Price Returns')
plt.show()


#-------------------------------------Part 4--------------------------------------


# Select components and relevant columns from listings
components = listings.loc[tickers, ['Market Capitalization', 'Last Sale']]

#Divide by 1 million of USD
components['Market Capitalization']/=1e6

# Print the first rows of components
print(components.head())

# Calculate the number of shares here
components['Number of Shares'] = components['Market Capitalization'].div(components['Last Sale'])

no_shares=components['Number of Shares']
print(no_shares.sort_values())

# Create the series of market cap per ticker
market_cap = stock_prices.mul(no_shares)

# Select first and last market cap here
first_value = market_cap.iloc[0]
last_value = market_cap.iloc[-1]


# Concatenate and plot first and last market cap here
pd.concat([first_value,last_value], axis=1).plot(kind='barh')
plt.show()


#---------------------------------------Part 6-----------------------------------


# Aggregate and print the market cap per trading day
raw_index = market_cap.sum(axis=1)
print(raw_index)

# Normalize the aggregate market cap here 
index = raw_index.div(raw_index.iloc[0]).mul(100)
print(index)

# Plot the index here
index.plot(title='Market-Cap Weighted Index')
plt.show()

#-----------------------------------------Evaluate Index Performance



pip install yfinance matplotlib pandas

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch historical stock data (e.g., Apple)
ticker = 'AAPL'
stock_data = yf.download(ticker, start='2020-01-01', end='2023-01-01')

# Display the first few rows of data
print(stock_data.head())

# Calculate the short-term (20-day) and long-term (50-day) moving averages
stock_data['20_MA'] = stock_data['Close'].rolling(window=20).mean()
stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()

# Drop NaN values
stock_data = stock_data.dropna()

# Display the first few rows with the moving averages
print(stock_data[['Close', '20_MA', '50_MA']].head())

# Create buy and sell signals
stock_data['Signal'] = 0
stock_data['Signal'][20:] = np.where(stock_data['20_MA'][20:] > stock_data['50_MA'][20:], 1, 0)  # 1 for buy, 0 for sell
stock_data['Position'] = stock_data['Signal'].diff()

# Display the signals
print(stock_data[['Close', '20_MA', '50_MA', 'Signal', 'Position']].tail())

# Plot the stock price with moving averages and signals
plt.figure(figsize=(12,6))

# Plot the closing price and moving averages
plt.plot(stock_data['Close'], label='Close Price', alpha=0.5)
plt.plot(stock_data['20_MA'], label='20-Day Moving Average', color='green', alpha=0.75)
plt.plot(stock_data['50_MA'], label='50-Day Moving Average', color='red', alpha=0.75)

# Plot buy signals
plt.plot(stock_data[stock_data['Position'] == 1].index,
         stock_data['20_MA'][stock_data['Position'] == 1],
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot sell signals
plt.plot(stock_data[stock_data['Position'] == -1].index,
         stock_data['20_MA'][stock_data['Position'] == -1],
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title(f'{ticker} Trading Strategy (Mean Reversion)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='best')
plt.grid()
plt.show()

# Calculate returns from holding the stock
stock_data['Returns'] = stock_data['Close'].pct_change()

# Calculate strategy returns based on the signals
stock_data['Strategy_Returns'] = stock_data['Returns'] * stock_data['Signal'].shift(1)

# Cumulative returns
stock_data['Cumulative_Strategy_Returns'] = (1 + stock_data['Strategy_Returns']).cumprod()

# Plot cumulative returns
plt.figure(figsize=(10,6))
plt.plot(stock_data['Cumulative_Strategy_Returns'], label='Strategy Returns')
plt.title(f'{ticker} Cumulative Strategy Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend(loc='best')
plt.grid()
plt.show()

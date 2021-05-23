# Here we do technical analysis with help of Ai and statistics models
import pandas as pd
import requests
import ta# TA's RSI 

#Due to Heroku restrictions, we need to store date on other clouds and pass its link
url = "https://drive.google.com/file/d/1WZzdZBT4QSrLKWHmA1KRUVm-AKE-LOGK/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)
print(df.head())

# Datetime conversion
df['Date'] = pd.to_datetime(df.Date)# Setting the index
df.set_index('Date', inplace=True)

# Importing Library

df['ta_rsi'] = ta.momentum.rsi(df.Close)# TA's Stochastic Oscillator
df['ta_stoch_k'] = ta.momentum.stoch(df.High, df.Low, df.Close)
df['ta_stoch_d'] = ta.momentum.stoch_signal(df.High, df.Low, df.Close)

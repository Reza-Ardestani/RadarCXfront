# Here we do technical analysis with help of Ai and statistics
import requests
import numpy as np
import pandas as pd
import yfinance as yf
import ta

''' For the time being we pass data via global var, Upgrate it by using DB'''
global Current_day_tech_signal


def loadFromGoogleDrive(url = None):
    #Due to Heroku restrictions, we need to store date on other clouds and pass its link
    # loading csv data from googleDrive
    if url == None:
        url = "https://drive.google.com/file/d/1WZzdZBT4QSrLKWHmA1KRUVm-AKE-LOGK/view?usp=sharing"

    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df.Date)# Setting the index
    df.set_index('Date', inplace=True)# Datetime conversion

    return df

def loadFrom_yfinance(tickers ='BTC-USD' , period='1mo', interval='1d'):
    # Using yahooFinance! API to fetch price of stocks
    df = yf.download(tickers=tickers,period=period,interval=interval)

    return df

def technicalCalculations(dt):
    ''' using ta to do some technical analysis '''
    dt['ta_rsi'] = ta.momentum.rsi(dt.Close)
    # TA's Stochastic Oscillator
    dt['ta_stoch_k'] = ta.momentum.stoch(dt.High, dt.Low, dt.Close)
    dt['ta_stoch_d'] = ta.momentum.stoch_signal(dt.High, dt.Low, dt.Close)

def elicitSignals(df):
    global Current_day_tech_signal
    # implementing naive RSI based elicitSignals
    rsi = df['ta_rsi'].iloc[-1] # current day rsi
    if rsi > 80:
        Current_day_tech_signal = "Strong Sell"
    elif rsi > 65:
         Current_day_tech_signal = "Sell"
    elif rsi > 45:
        Current_day_tech_signal = "Neutral"
    elif rsi > 25:
        Current_day_tech_signal = "Buy"
    else:
        Current_day_tech_signal = " Strong Buy"

def tech_signal():
    # based on daily data, we provide signals for bitcoin
    # the result will be available on "Current_day_tech_signal"
    print(" before loop :", Current_day_tech_signal)
    while(True):
        # for the time being, we use yfinance as the source of data
        df = loadFrom_yfinance()
        print(" after loadFrom_yfinance :", Current_day_tech_signal)
        #Using ta for tech analysis
        technicalCalculations(df)
        print(" after technicalCalculations func  :", Current_day_tech_signal)
        # based on  our meta-knowlege we elicit signals out of data
        # the result will be stored in "Current_day_tech_signal"
        elicitSignals(df)
        print(" Final ai tech result:", Current_day_tech_signal)
        sleep(3600)

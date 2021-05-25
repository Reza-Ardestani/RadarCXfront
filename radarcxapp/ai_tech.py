# Here we do technical analysis with help of Ai and statistics
import requests
import numpy as np
import pandas as pd
import yfinance as yf
import ta

''' For the time being we pass data via global var, Upgrate it by using DB'''
global Current_day_tech_signal


def load_from_googleDrive(url = None):
    #Due to Heroku restrictions, we need to store date on other clouds and pass its link
    # loading csv data from googleDrive
    if url == None:
        url = "https://drive.google.com/file/d/1WZzdZBT4QSrLKWHmA1KRUVm-AKE-LOGK/view?usp=sharing"

    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df.Date)# Setting the index
    df.set_index('Date', inplace=True)# Datetime conversion

    return df
def load_from_yfinance():
    pass


def tech_signal():
    # based on daily data, we provide signals for bitcoin
    # the result will be available on "Current_day_tech_signal"
    pass

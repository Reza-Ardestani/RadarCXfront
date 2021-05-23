# Here we do technical analysis with help of Ai and statistics models
import pandas as pd
import requests

url = "https://drive.google.com/file/d/1WZzdZBT4QSrLKWHmA1KRUVm-AKE-LOGK/view?usp=sharing"
df = pd.read_csv(url)
print(df.head())

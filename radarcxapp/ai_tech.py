# Here we do technical analysis with help of Ai and statistics models
import pandas as pd
import requests

#Due to Heroku restrictions, we need to store date on other clouds and pass its link
url = "https://drive.google.com/file/d/1WZzdZBT4QSrLKWHmA1KRUVm-AKE-LOGK/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)
print(df.head())

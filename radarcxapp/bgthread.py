from os import spawnve
import time, requests, threading
from .models import Coin, Condition
from radarcx import settings
from .notif import *
from radarcxapp.models import *

#string_test = "logs:\n"



coins = ['BTC', 'ETH', 'BNB', 'ADA', 'DOGE', 'XRP', 'DOT',
 'ICP', 'BCH', 'UNI', 'LTC', 'LINK', 'MATIC', 'SOL', 'XLM',
 'VET', 'ETC', 'THETA', 'EOS', 'TRX', 'FIL', 'NEO', 'CRV']


def conditionsChecker():
    #here we check whether any of conditions has been triggerd or #
    ''' note: we have not implemented 'equal' and 'moving_average','volume' yet. '''
    conditions = Condition.objects.all()
    for condition in conditions:
        coin_quantity = Coin.objects.filter(name=condition.coin).last().realtime_price
        if (condition.triggered == True):
            continue
        if condition.smaller_or_greater == ">" and coin_quantity >= condition.quantity :
            username = User.objects.filter(id=condition.creator_id).first()
            coinName= condition.coin
            Bodytext = coinName + " is now " + str(coin_quantity) + "$ --- ( > " + str(condition.quantity) + "$ )"
            user  = User.objects.filter(id=condition.creator_id).first()
            usertokens = user.usertoken_set.all()
            one_user_tokens = [ record.token for record in usertokens ]
            NajveResponse = send_to_users(body= Bodytext,
            subscriber_tokens= one_user_tokens,
            sent_time=UTC_to_IR_TimeZone())
            condition.triggered = True
            condition.save()
        elif condition.smaller_or_greater == "<" and coin_quantity <= condition.quantity :
            username = User.objects.filter(id=condition.creator_id).first()
            coinName= condition.coin
            Bodytext = coinName + " is now " + str(coin_quantity) + "$ --- ( < " + str(condition.quantity) + "$ )"
            user  = User.objects.filter(id=condition.creator_id).first()
            usertokens = user.usertoken_set.all()
            one_user_tokens = [ record.token for record in usertokens ]
            NajveResponse = send_to_users(body= Bodytext,
            subscriber_tokens= one_user_tokens,
            sent_time=UTC_to_IR_TimeZone())
            condition.triggered = True
            condition.save()



def fetchData_and_check():
    ''' In this part we check whether for every coin that we
        support , there exist a single record in our coins table or not
        This is temporary. The best way to do this is by using "signal"
        concept in django.

        the way that we do this, is by chekcing that we have a rocord for
        ,for instance, "BNB" or not. If we don't have we go through creating
        single record for all coins that doesn't have already

    '''
    coins = ['BTC', 'ETH', 'BNB', 'ADA', 'DOGE', 'XRP', 'DOT',
     'ICP', 'BCH', 'UNI', 'LTC', 'LINK', 'MATIC', 'SOL', 'XLM',
     'VET', 'ETC', 'THETA', 'EOS', 'TRX', 'FIL', 'NEO', 'CRV']

    testObj = Coin.objects.filter(name="BNB").first()
    if (not (testObj) ):
        for coinName in coins:
            tmp = Coin.objects.filter(name=coinName).first()
            if (not (tmp)):
                initiating_coin = Coin.objects.create(name=coinName)
                initiating_coin.save()

    while(True):
        # print("here I receive data of all coins and store them in DB")
        url = 'https://min-api.cryptocompare.com/data/price'
        parameters = {'fsym': "BTC",'tsyms': "USD"}
        ''' getting data and storing them in DB '''
        # response comes as json
        for nameOfCoin in coins:
            parameters["fsym"] =nameOfCoin
            response = requests.get(url, params=parameters)
            data = response.json()
            c = Coin.objects.filter(name=parameters["fsym"]).first()
            c.realtime_price=data[parameters["tsyms"]]
            c.save()

        # Synchronizicly we runn this fun & wait till it ends
        conditionsChecker()
        time.sleep(300) # 300 sec

from os import spawnve
import time, requests, threading
from .models import Coin, Condition
from radarcx import settings
from .notif import *
from radarcxapp.models import *
#string_test = "logs:\n"


def conditionsChecker():
    #here we check whether any of conditions has been triggerd or #
    ''' note: we have not implemented 'equal' and 'moving_average','volume' yet. '''
    conditions = Condition.objects.all()
    for condition in conditions:
        coin_quantity = Coin.objects.filter(name=condition.coin).last()
        user  = User.objects.filter(id=condition.creator_id).first()
        usertokens = user.usertoken_set.all()
        print(usertokens)

        if condition.smaller_or_greater == "g" and coin_quantity >= condition.quantity :
            #print(f"The {condition.type} of {condition.coin} is greater than {condition.quantity} ")
            username = User.objects.filter(id=condition.creator_id).first()
            coinName= condition.coin
            Bodytext = "Dear" + username + "your condition on"  + coinName +"at price"+condition.quantity + "has been triggered "
            user_token = ""
            NajveResponse = send_to_users(body= Bodytext,
            subscriber_tokens=[user_token],
            sent_time=UTC_to_IR_TimeZone())

        if condition.smaller_or_greater == "s" and coin_quantity <= condition.quantity :
            print(f"The {condition.type} of {condition.coin} is smaller than {condition.quantity} ")



def fetchData_and_check():
    conditionsChecker()
    '''
    while(True):
        # startOfLoopTime = perf_counter()
        # print("here I receive data of all coins and store them in DB")
        url = 'https://min-api.cryptocompare.com/data/price'

        parameters = {'fsym': "BTC",
                    'tsyms': "USD"}
        exchange = ''

        if exchange:
            print('exchange: ', exchange)
            parameters['e'] = exchange

        # response comes as json
        response = requests.get(url, params=parameters)
        data = response.json()

        cleanup = Coin.objects.all()
        cleanup.delete()
        cleanup = Condition.objects.all()
        cleanup.delete()

        c = Coin(name="BTC", realtime_price=123, moving_average=123, volume=213)
        c.save()
        c = Coin.objects.get(name=parameters["fsym"])
        c.realtime_price=data[parameters["tsyms"]]
        c.save()

        conditionsChecker()  # Synchronizicly we runn this fun & wait till it ends
        '''
        # endOfLoopTime = perf_counter()
        # if(endOfLoopTime-startOfLoopTime < 60):
        #     sleep(round(endOfLoopTime-startOfLoopTime, 0))

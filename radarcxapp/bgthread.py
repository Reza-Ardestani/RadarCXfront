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
        print('im here in for of coditionCheker')
        coin_quantity = Coin.objects.filter(name=condition.coin).last().realtime_price
        if condition.smaller_or_greater == "greater_than" and coin_quantity >= condition.quantity :
            print('ipython pym here if')
            username = User.objects.filter(id=condition.creator_id).first()
            coinName= condition.coin
            Bodytext = "Dear" + username + "your condition on"  + coinName +"at price"+ str(condition.quantity) + "has been triggered "
            user  = User.objects.filter(id=condition.creator_id).first()
            usertokens = user.usertoken_set.all()
            one_user_tokens = [ record.token for record in usertokens ]
            NajveResponse = send_to_users(body= Bodytext,
            subscriber_tokens= one_user_tokens,
            sent_time=UTC_to_IR_TimeZone())
            print(NajveResponse)

        if condition.smaller_or_greater == "smaller_than" and coin_quantity <= condition.quantity :
            print('im here if') # testing puprose
            username = User.objects.filter(id=condition.creator_id).first()
            coinName= condition.coin
            Bodytext = "Dear" + username + "your condition on"  + coinName +"at price"+ str(condition.quantity) + "has been triggered "
            user  = User.objects.filter(id=condition.creator_id).first()
            usertokens = user.usertoken_set.all()
            one_user_tokens = [ record.token for record in usertokens ]
            NajveResponse = send_to_users(body= Bodytext,
            subscriber_tokens= one_user_tokens,
            sent_time=UTC_to_IR_TimeZone())
            print(NajveResponse)



def fetchData_and_check():
    print('im here in fetch data')
    while(True):
        conditionsChecker()
        time.sleep(60)
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

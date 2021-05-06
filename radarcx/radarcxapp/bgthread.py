import time, requests, threading
from .models import Coin, Condition

''' Start of threading'''
# Frist integration of multithreading part


def notifgeneral():
    pass


def notifSpecitic(userToken):
    # Notify user
    pass


def conditionsChecker():
    #here we check whether any of conditions has been triggerd or #
    
    # new thread realtimeprice_checker()
    conditions = Condition.objects.all()
    # if Coin.
    # new thread movingaverage_checker()

    # new thread volume_checker()


    # call "notifSpecitic" func if it's necessary
    pass


def fetchData_and_check():
    # print(user.objects.values())
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

        print(data)
        print(parameters["fsym"])
        print(data[parameters["tsyms"]])
        Coin(name=parameters["fsym"], realtime_price=data[parameters["tsyms"]], moving_average=123, volume=222).save()

        # return data

        conditionsChecker()  # Synchronizicly we runn this fun & wait till it ends

        # endOfLoopTime = perf_counter()
        # if(endOfLoopTime-startOfLoopTime < 60):
        #     sleep(round(endOfLoopTime-startOfLoopTime, 0))

''' End of threading '''

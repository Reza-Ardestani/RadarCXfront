import time, requests, threading
from .models import Coin, Condition
from radarcx import settings

string_test = "logs:\n"

''' Start of threading'''
# Frist integration of multithreading part

def listOfClients():
    from najva_api_client.najva import Najva
    client = Najva()
    client.apikey = "9e48e9f0-41e1-4f0a-a3d0-dd34b8313f03"
    client.token = "4fa9220c03c0483ccd5dbced0b83a78c9e242e3f"

    # getting all connected clients to our website
    accounts_str = client.get_onesignal_accounts()
    string_test += (accounts_str) + '\n'

def notifgeneral():
    pass


def notifSpecific(userToken):
    # Notify user
    pass


def conditionsChecker():
    #here we check whether any of conditions has been triggerd or #

    # new thread realtimeprice_checker()
    conditions = Condition.objects.filter(type="price", smaller_or_greater="greater")

    for condition in conditions :
        coin = condition.coin
        realtime_price = Coin.objects.filter(name=coin).last().realtime_price
        quantity = condition.quantity

        if realtime_price >= quantity :
            #call "notifSpecitic" func
            print("price greater")
            pass

    conditions = Condition.objects.filter(type="price", smaller_or_greater="smaller")

    for condition in conditions :
        coin = condition.coin
        realtime_price = Coin.objects.filter(name=coin).last().realtime_price
        quantity = condition.quantity

        if realtime_price <= quantity :
            #call "notifSpecitic" func
            print("price smaller")
            pass

    # new thread movingaverage_checker()
    conditions = Condition.objects.filter(type="moving_average", smaller_or_greater="smaller")

    for condition in conditions :
        coin = condition.coin
        moving_average = Coin.objects.filter(name=coin).last().moving_average
        quantity = condition.quantity

        if moving_average <= quantity :
            #call "notifSpecitic" func
            print("moving_average smaller")
            pass

    conditions = Condition.objects.filter(type="moving_average", smaller_or_greater="greater")

    for condition in conditions :
        coin = condition.coin
        moving_average = Coin.objects.filter(name=coin).last().moving_average
        quantity = condition.quantity

        if moving_average >= quantity :
            #call "notifSpecitic" func
            print("moving_average greater")
            pass


    # new thread volume_checker()
    conditions = Condition.objects.filter(type="volume", smaller_or_greater="smaller")

    for condition in conditions :
        coin = condition.coin
        volume = Coin.objects.filter(name=coin).last().volume
        quantity = condition.quantity

        if volume <= quantity :
            #call "notifSpecitic" func
            print("volume smaller")
            pass

    conditions = Condition.objects.filter(type="volume", smaller_or_greater="greater")

    for condition in conditions :
        coin = condition.coin
        volume = Coin.objects.filter(name=coin).last().volume
        quantity = condition.quantity

        if volume >= quantity :
            #call "notifSpecitic" func
            print("volume greater")
            pass

    pass


def fetchData_and_check():
    global string_test
    # print(user.objects.values())
    listOfClients()
    #sleep(60) #remove this line later _matthew_
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

        # print(data)
        # print(parameters["fsym"])
        # print(data[parameters["tsyms"]])
        #Coin(name=parameters["fsym"], realtime_price=data[parameters["tsyms"]], moving_average=123, volume=222).save()

        # return data

        conditionsChecker()  # Synchronizicly we runn this fun & wait till it ends

        # endOfLoopTime = perf_counter()
        # if(endOfLoopTime-startOfLoopTime < 60):
        #     sleep(round(endOfLoopTime-startOfLoopTime, 0))

''' End of threading '''


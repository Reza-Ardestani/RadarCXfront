from os import spawnve
import time, requests, threading
from .models import Coin, Condition
from radarcx import settings

string_test = "logs:\n"

''' Start of threading'''
# Frist integration of multithreading part

def iranTimeZone(delay = 0):
    # time should be in this format :"%Y-%m-%dT%H:%M:%S"
    pass

def get_onesignal_accounts():
    # rename listOfClients to get_onesignal_accounts
    #based on Najva's Docs, this func return googleAnalyt, firebase, and
    #other connected accounts
    # this function return list of listOf_onesignal_accounts
    from najva_api_client.najva import Najva
    client = Najva()
    client.apikey = "9e48e9f0-41e1-4f0a-a3d0-dd34b8313f03"
    client.token = "6e83d4164baf569f345ab556b01347b1178776c5"

    # getting all connected clients to our website
    accounts_str = client.get_onesignal_accounts()
    string_test += (accounts_str) + '\n'

def notifAll(titleText , bodyText):
    # notifying all users
    # make sure title and body are str

    client = Najva()
    client.apikey = "9e48e9f0-41e1-4f0a-a3d0-dd34b8313f03"
    client.token = "6e83d4164baf569f345ab556b01347b1178776c5"
    notifAll_response = client.send_to_all(title=titleText,
    body=bodyText,
    url="https://radarcx.herokuapp.com/",
    icon="https://png.pngtree.com/element_our/md/20180515/md_5afb099d307d3.jpg",
    image="https://png.pngtree.com/element_our/md/20180515/md_5afb099d307d3.jpg",
    onclick="open-link",
    one_signal_enabled=False,)

    return notifAll_response


def notifSpecific(userToken , titleText , bodyText ):
    #make sure userToken is str and in other forms
    from najva_api_client.najva import Najva
    # Najve requirements for the Notify_specific_user:
    #send_to_users(self,title, body, url, icon,subscriber_tokens,
    #              onclick='open-link', image=None,
    #              content=None,json=None,sent_time=None):
    client = Najva()
    client.apikey = "9e48e9f0-41e1-4f0a-a3d0-dd34b8313f03"
    client.token = "6e83d4164baf569f345ab556b01347b1178776c5"

    notifSpecific_response = client.send_to_users(title=titleText,
    body= bodyText,
    url="https://radarcx.herokuapp.com/",
    icon="https://png.pngtree.com/element_our/md/20180515/md_5afb099d307d3.jpg",
    image="https://png.pngtree.com/element_our/md/20180515/md_5afb099d307d3.jpg",
    onclick="open-link",
    subscriber_tokens=[userToken])

    return notifSpecific_response


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

    MattewsToken = '8d705edd-f193-4f5a-a9d5-d63e802f2fb3'
    MattewsTokenNum2 = '1ba8d7be-5038-4754-8f3a-7f0e902f6c4e'

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

        # endOfLoopTime = perf_counter()
        # if(endOfLoopTime-startOfLoopTime < 60):
        #     sleep(round(endOfLoopTime-startOfLoopTime, 0))

''' End of threading '''

import threading
import time

''' Start of threading'''
# Frist integration of multithreading part


def notifgeneral():
    pass


def notifSpecitic(userToken):
    # Notify user
    pass


def conditionsChecker():
    #here we check whether any of conditions has been triggerd or #

    # call "notifSpecitic" func if it's necessary
    pass


def fetchData_and_check():
    # print(user.objects.values())
    while(True):
        startOfLoopTime = perf_counter()
        print("here I receive data of all coins and store them in DB")
        url = 'https://min-api.cryptocompare.com/data/price'

    parameters = {'fsym': from_sym,
                  'tsyms': to_sym}

    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange
    # response comes as json
    response = requests.get(url, params=parameters)
    data = response.json()

    return data

    conditionsChecker()  # Synchronizicly we runn this fun & wait till it ends

    endOfLoopTime = perf_counter()
    if(endOfLoopTime-startOfLoopTime < 60):
        sleep(round(endOfLoopTime-startOfLoopTime, 0))


# doing work
coinsData_thread = threading.Thread(target=fetchData_and_check)
coinsData_thread.start()
# print("last line of main process")
''' End of threading '''

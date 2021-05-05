from django.shortcuts import render
# for using temporary html file, showing to users
from django.http import HttpResponse
from .models import *

def coinlist(request):
    return render(request, 'result.html')
    #return HttpResponse('<h1>Blog home</h1>')
def conditions(request):
    return render(request, 'conditions.html')

''' Start of threading'''
## Frist integration of multithreading part
import time
import threading

def conditionsChecker():
    #here we check whether any of conditions has been triggerd or #
    ##print("i'm in conditions cheker function")
    # call notification func if it's necessary
    pass

def fetchData_and_check():
    print(user.objects.values())
    #while(True):
    #    #startTime = perf_counter()
    #    ##print("here I receive data of all coins and store them in DB")
    #    time.sleep(3)
    #    conditionsChecker()#Synchronizicly we runn this fun & wait till it ends
    #    time.sleep(1)

# doing work
#coinsData_thread = threading.Thread(target= fetchData_and_check )
#coinsData_thread.start()
# print("last line of main process")
''' End of threading '''

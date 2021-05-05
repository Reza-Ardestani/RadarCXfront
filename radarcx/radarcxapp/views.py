from django.shortcuts import render
# for using temporary html file, showing to users
from django.http import HttpResponse
from .models import *

# To use class based views
from django.views.generic import View

def coinlist(request):
    return render(request, 'result.html')
    #return HttpResponse('<h1>Blog home</h1>')
def conditions(request):
    print(request)
    return render(request, 'conditions.html')

# Start of new conditions capturing ---> '/new_cond
class new_cond(View):
    def get(self, request):
        return HttpResponse("We do not have GET at this URL")
    def post(self, request):
        c = Condition()
        c.type = request.POST["cond_type"]
        c.quantity = request.POST["amount"]
        c.coin = request.POST["coin"]
        c.smaller_or_greater = request.POST["trigger"]
        c.save()
        print(Condition.objects.all())
        # print (request.POST)
        return HttpResponse("Your condition added successfully!")
# End of new condition capturing ---> '/new_cond


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

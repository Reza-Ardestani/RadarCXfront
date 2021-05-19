from django.shortcuts import render,redirect

# for using temporary html file, showing to users
from django.http import HttpResponse
from .models import *

# To use class based views
from django.views.generic import View

# To use threading used by Morty
from . import bgthread
import threading

# to use simple json
import os

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import ListView

def coins(request):
    coins = Coin.objects.all()
    context = {'coins' : coins}
    res = render(request, 'radarcxapp/coins.html', context)
    # res['Access-Control-Allow-Origin'] = '*'
    return res

@login_required
def conditions(request):
    context = {
        #'conditions' : Condition.objects.get(creator=user)
    }
    return render(request, 'radarcxapp/conditions.html', context)
 
class ConditionListView(ListView):
    model = Condition
    template_name = 'radarcxapp/conditions.html'
    context_object_name = 'conditions'

     

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
        #c.save()
        # print(Condition.objects.all())
        # print (request.POST)
        messages.success(request, "Your condition added successfully!")
        return redirect('conditions')
# End of new condition capturing ---> '/new_cond

# coinsData_thread = threading.Thread(target=bgthread.fetchData_and_check)
# coinsData_thread.start()


# manifest.json handler

from radarcx import settings
import json
from django.http import JsonResponse
def manifest(request):
    manifest_file = open(os.path.join(settings.BASE_DIR, 'manifest.json'))
    #print(json.load(manifest_file))
    return JsonResponse(json.load(manifest_file))


# najva-messaging-sw.js handler

from radarcx import settings
def sw(request):
    sw_file = open(os.path.join(settings.BASE_DIR, 'najva-messaging-sw.js'))
    return HttpResponse(sw_file.read(), headers={'content-type': 'application/javascript; charset=utf-8'})


# def log(request):
#     return HttpResponse(bgthread.string_test)

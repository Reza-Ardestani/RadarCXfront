from django.shortcuts import render,redirect

# for using temporary html file, showing to users
from radarcxapp.models import *

# To use class based views
from django.views.generic import View

# To use threading used by Morty
from . import bgthread
import threading

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from django.views.generic import ListView

def coins(request):
    user = request.user
    if user.is_authenticated:
        username = request.user
        user  = User.objects.filter(username=username).first()
        coins = user.favoritecoins_set.all()
        context = {'coins' : coins}
        return render(request, 'radarcxapp/coins.html', context)

    else:
        coins = Coin.objects.all()
        context = {'coins' : coins}
        return render(request, 'radarcxapp/coins.html', context)

@login_required
def conditions(request):
    username = request.user
    user  = User.objects.filter(username=username).first()
    conditions = user.condition_set.all()
    context = {
       'title' : 'Conditions',
        'conditions' : conditions
    }
    return render(request, 'radarcxapp/conditions.html', context)

# Start of new conditions capturing ---> '/new_cond
class new_cond(View):
    def post(self, request):
        username = request.user
        user  = User.objects.filter(username=username).first()
        c = Condition()
        c.name = request.POST["cond_name"]
        c.type = request.POST["cond_type"]
        c.quantity = request.POST["amount"]
        c.coin = request.POST["coin"]
        c.smaller_or_greater = request.POST["trigger"]
        c.creator = user
        c.save()
        messages.success(request, "Your condition added successfully!")
        return redirect('conditions')
# End of new condition capturing ---> '/new_cond


# Singnals
def signals(request):
    return render(request, 'radarcxapp/signals.html')

# manifest.json handler
from radarcx import settings
import os, json
from django.http import JsonResponse, HttpResponse
def manifest(request):
    manifest_file = open(os.path.join(settings.BASE_DIR, 'manifest.json'))
    return JsonResponse(json.load(manifest_file))


# najva-messaging-sw.js handler
from radarcx import settings
def sw(request):
    sw_file = open(os.path.join(settings.BASE_DIR, 'najva-messaging-sw.js'))
    return HttpResponse(sw_file.read(), headers={'content-type': 'application/javascript; charset=utf-8'})


# getting najva token from user's browser
def najva_token(request):
    print(request.headers)
    if request.user.is_authenticated:
        t = UserToken(user=request.user, token=request.headers['SHIT'])
        t.save()
    return HttpResponse("you shit")

# coinsData_thread = threading.Thread(target=bgthread.fetchData_and_check)
# coinsData_thread.start()

# chk url
def chk(request):
    bgthread.fetchData_and_check()
    return HttpResponse("Conditions table has been manually check!")

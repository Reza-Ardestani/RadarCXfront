from django.shortcuts import render,redirect

# for using temporary html file, showing to users
from radarcxapp.models import *

# To use class based views
from django.views.generic import View

# To use threading used by Morty
from . import bgthread
from . import ai_tech
import threading

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from django.views.generic import ListView

def coins(request):
    all_coins = Coin.objects.all()
    if request.user.is_authenticated:
        username = request.user
        user  = User.objects.filter(username=username).first()
        fav_coins = user.favoritecoins_set.all()
        fcoins = []
        for c in fav_coins:
            fcoins.append(c.favorite_coin)
        print(fcoins)
        fav_coins = fcoins
        all_coins = Coin.objects.values_list("name").difference(user.favoritecoins_set.values_list('favorite_coin__name'))
    else:
        fav_coins = all_coins
    context = {'fav_coins' : fav_coins, 'all_coins' : all_coins}
    return render(request, 'radarcxapp/coins.html', context)


# Start of deleting coin by user ---> '/delete_coin
class delete_coin(View):
    def post(self, request):
        username = request.user
        user  = User.objects.filter(username=username).first()
        favorite_coin_name = request.POST["coin"]
        favorite_coin = FavoriteCoins.objects.filter(user=user,favorite_coin__name=favorite_coin_name).last()
        favorite_coin.delete()
        messages.success(request, "The coin deleted successfully!")
        return redirect('coins')
# End of deleting coin by user ---> '/delete_coin


# Start of adding coin by user ---> '/add_coin
class add_coin(View):
    def post(self, request):
        username = request.user
        user  = User.objects.filter(username=username).first()
        f_coin = FavoriteCoins()
        f_coin.user = user
        favorite_coin = request.POST["coin"]
        coin = Coin.objects.filter(name=favorite_coin).first()
        f_coin.favorite_coin = coin
        f_coin.save()
        messages.success(request, "Your favorite coin added successfully!")
        return redirect('coins')
# End of adding coin by user ---> '/add_coin


@login_required
def conditions(request):
    username = request.user
    user  = User.objects.filter(username=username).first()
    conditions = user.condition_set.all()
    all_coins = Coin.objects.all()
    context = {
        'title' : 'Conditions',
        'conditions' : conditions,
        'coins' : all_coins
    }
    return render(request, 'radarcxapp/conditions.html', context)

# Start of new conditions capturing ---> '/new_cond
class new_cond(View):
    def post(self, request):
        username = request.user
        user  = User.objects.filter(username=username).first()
        c = Condition()
        c.name = request.POST["cond_name"]
        if c.name == '':
            messages.error(request, "Condition name is required!")
            return redirect('conditions')
        c.type = request.POST["cond_type"]
        if request.POST["amount"] == '':
            messages.error(request, "Enter the targeted price!")
            return redirect('conditions')
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
    if request.user.is_authenticated:
        najva = token=request.headers['najva-token']
        if len(UserToken.objects.filter(token=najva))==0:
            t = UserToken(user=request.user, token=najva)
            t.save()
    return HttpResponse("you shit")



####
# chk url , this url make fetchData_and_check run one time
''' fetchData_and_check func has a not ending loop,
    so we should only run it one time with the help of following global var'''
fetchData_and_check_status = "notRunning"

''' initiating fetchData_and_check func thread '''
coinsData_thread = threading.Thread(target=bgthread.fetchData_and_check)

def chk(request):
    global fetchData_and_check_status
    if fetchData_and_check_status == "notRunning":
        fetchData_and_check_status = "running"
        # bgthread.fetchData_and_check() // wrong, we need a thread
        coinsData_thread.start()
    return HttpResponse("Conditions table has been manually check!")

####
ai_tech_status = "notRunning"
technical_signal_thread = threading.Thread(target=ai_tech.tech_signal)
def ai_tech(request):
    global ai_tech_status
    if ai_tech == "notRunning":
        technical_signal_thread.start()
        ai_tech_status = "running"
    return HttpResponse("Technical signal has been manually started!")


#####

def overall(request):
    return render(request, 'radarcxapp/overall.html')

def technical(request):
    return render(request, 'radarcxapp/technical.html')

def fundamental(request):
    return render(request, 'radarcxapp/fundamental.html')

def sentiment(request):
    return render(request, 'radarcxapp/sentiment.html')

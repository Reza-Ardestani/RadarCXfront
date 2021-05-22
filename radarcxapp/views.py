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
        all_coins = Coin.objects.all()
        context = {'coins' : coins, 'all_coins' : all_coins}
        return render(request, 'radarcxapp/coins.html', context)

    else:
        coins = [
            'BTC', 'ETH', 'BNB', 'ADA', 'DOGE', 'XRP', 'DOT', 'ICP', 'BCH',
            'UNI', 'LTC', 'LINK', 'MATIC', 'SOL', 'XLM', 'VET', 'ETC', 'THETA',
            'EOS', 'TRX', 'FIL', 'NEO', 'CRV'
        ]
        context = {'coins' : coins}
        return render(request, 'radarcxapp/coins.html', context)


# Start of deleting coin by user ---> '/delete_coin
class delete_coin(View):
    def post(self, request):
        username = request.user
        user  = User.objects.filter(username=username).first()
        favorite_coin_name = request.POST["coin"]
        favorite_coin = FavoriteCoins.objects.filter(user=user,favorite_coin__name=favorite_coin_name).last()
        favorite_coin.delete()
        messages.success(request, "Your wanted coin deleted successfully!")
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
    if request.user.is_authenticated:
        najva = token=request.headers['SHIT']
        if len(UserToken.objects.filter(token=najva))==0:
            t = UserToken(user=request.user, token=najva)
            t.save()
    return HttpResponse("you shit")

# coinsData_thread = threading.Thread(target=bgthread.fetchData_and_check)
# coinsData_thread.start()

# chk url , this url make fetchData_and_check run one time
def chk(request):
    bgthread.fetchData_and_check()
    return HttpResponse("Conditions table has been manually check!")

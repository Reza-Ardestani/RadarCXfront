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
        messages.success(request, "The coin is deleted successfully!")
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
        messages.success(request, "Your favorite coin has been added successfully!")
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
        messages.success(request, "Your condition has been added !")
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


# deleting a condition
def del_cond(request):
    cond_id = request.POST["cond_id"]
    cond = Condition.objects.filter(id=cond_id).first()
    cond.delete()
    messages.success(request, "The condition deleted successfully!")
    return redirect('conditions')


####
# chk url , this url make fetchData_and_check run one time
''' fetchData_and_check func has a not ending loop,
    so we should only run it one time with the help of following global var'''

fetchData_and_check_status = "notRunning"
''' initiating fetchData_and_check func thread '''
coinsData_thread = threading.Thread(target=bgthread.fetchData_and_check)

# Heroku kill all threads after being 30 min idle
# so we need to create them for each start up:

if fetchData_and_check_status == "notRunning":
    # "if" is somehow redundent(added for improving clarity)
    ''' comment next line in your local machine if you'd like'''
    ''' But Do not forget to uncomment it on the server '''
    coinsData_thread.start()
    fetchData_and_check_status = "running"

def chk(request):
    global fetchData_and_check_status
    if fetchData_and_check_status == "notRunning":
        fetchData_and_check_status = "running"
        # bgthread.fetchData_and_check() // wrong, we need a thread
        coinsData_thread.start()
        return HttpResponse("Conditions table checker has been manually started!")

    return HttpResponse("Conditions table checker is already running!")

####
ai_tech_status = "notRunning"
technical_signal_thread = threading.Thread(target=ai_tech.tech_signal)

# Heroku kill all threads after being 30 min idle
# so we need to create them for each start up:

if ai_tech_status == "notRunning":
    # "if" is somehow redundent(added for improving clarity)
    ''' comment next line in your local machine if you'd like'''
    ''' But Do not forget to uncomment it on the server '''
    technical_signal_thread.start()
    ai_tech_status = "running"


def ai_tech(request):
    global ai_tech_status
    if ai_tech_status == "notRunning":
        technical_signal_thread.start()
        ai_tech_status = "running"
        return HttpResponse("Technical signal has been manually started!")

    return HttpResponse("Technical signal is already running!")


#####

def overall(request):
    return render(request, 'radarcxapp/overall.html')
#####
from .ai_tech import Current_day_tech_signal

def technical(request):
    global Current_day_tech_signal
    color = ''
    if (Current_day_tech_signal == "Strong Sell"):
        color = 'danger'
    elif (Current_day_tech_signal == "Sell"):
        color = 'warning'
    elif (Current_day_tech_signal == "Neutral"):
        color = 'success'
    elif (Current_day_tech_signal == "Buy"):
        color = 'info'
    elif (Current_day_tech_signal == "Strong Buy"):
        color = 'primary'

    context = {
        'Current_day_tech_signal' : Current_day_tech_signal[0],
        'color': color,
    }
    return render(request, 'radarcxapp/technical.html',context)

####
def fundamental(request):
    return render(request, 'radarcxapp/fundamental.html')

def sentiment(request):
    return render(request, 'radarcxapp/sentiment.html')

def about(request):
    return render(request, 'radarcxapp/about.html')

def contact_us(request):
    return render(request, 'radarcxapp/contact_us.html')

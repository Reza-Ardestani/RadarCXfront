from django.shortcuts import render,redirect

''' testing purpose'''
from .notif import *

#notifSpecific_response = send_to_users(body= "May 20th Heroku test",
#ubscriber_tokens=['476f636f-ceda-470a-b8de-2ed4c32f5a3d','6685a775-c3a4-418b-af80-cc7c31eac2f5'],
#sent_time=UTC_to_IR_TimeZone())

#print("Najjjjjva response:",notifSpecific_response)
'''End test '''
# for using temporary html file, showing to users
from radarcxapp.models import *

# To use class based views
from django.views.generic import View

# To use threading used by Morty
from . import bgthread
import threading

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import ListView

def coins(request):
    coins = Coin.objects.all()
    context = {
        'title' : 'Coins',
        'coins' : coins
    }
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

#class ConditionListView(ListView):
#    model = Condition
#    template_name = 'radarcxapp/conditions.html'
#    context_object_name = 'conditions'

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

coinsData_thread = threading.Thread(target=bgthread.fetchData_and_check)
coinsData_thread.start()

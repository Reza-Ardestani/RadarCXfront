from django.conf.urls import url

from radarcxapp import views

urlpatterns = [
    url('', views.coinlist, name='coinlist')
]
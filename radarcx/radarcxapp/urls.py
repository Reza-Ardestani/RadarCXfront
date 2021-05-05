from django.conf.urls import url

from radarcxapp import views

urlpatterns = [
    url('^$', views.result, name='result'),
    url('result', views.result, name='result'),
    url('conditions', views.conditions, name='conditions'),
    url('new_cond', views.new_cond.as_view(), name='new_cond'),
]

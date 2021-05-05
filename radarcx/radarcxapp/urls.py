from django.conf.urls import url

from radarcxapp import views

urlpatterns = [
    url('^$', views.coinlist, name='coinlist'),
    url('conditions', views.conditions, name='conditions'),
    url('new_cond', views.new_cond.as_view(), name='new_cond'),

]

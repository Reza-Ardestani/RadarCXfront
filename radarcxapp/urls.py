from django.conf.urls import url
from .views import ConditionListView
from radarcxapp import views

urlpatterns = [
    url('^$', views.coins, name='coins'),
    url('coins', views.coins, name='coins'),
    url('conditions', ConditionListView.as_view(), name='conditions'),
    url('new_cond', views.new_cond.as_view(), name='new_cond'),
    url('manifest.json', views.manifest, name='manifest'),
    url('najva-messaging-sw.js', views.sw, name='sw'),
    # url('log', views.log, name='log'),
]

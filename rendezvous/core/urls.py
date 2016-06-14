from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    # ex: /about/
    url(r'^about/$', views.about, name='about'),
    # ex: /login/
    url(r'^login/$', views.login, name='login'),
    # ex: /logout/
    url(r'^logout/$', views.logout, name='logout'),

    # ex: /brokers/
    url(r'^brokers/$', views.brokers, name='brokers'),
    # ex: /brokers/del/1
    url(r'^brokers/del/(?P<pk>[0-9]+)/$', views.broker_del, name='deleteBroker'),
]

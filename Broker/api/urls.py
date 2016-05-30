from django.conf.urls import include, url
from api import views
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView
from core.models import Service, Broker
from core.serializers import ServiceSerializer, BrokerSerializer


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),


    # url(r'^serv/$', views.ServicesList.as_view()),
    # url(r'^services/$', views.getservices),

    # ex: api/services/
    url(r'^services/$', ListCreateAPIView.as_view(queryset=Service.objects.all(), serializer_class=ServiceSerializer),
        name='services-list'),

    # ex: api/services/1
    url(r'^services/del/(?P<pk>[0-9]+)$', DestroyAPIView.as_view(queryset=Service.objects.all(), serializer_class=ServiceSerializer),
        name='services-del'),

    # ex: api/brokers/
    url(r'^brokers/$', ListAPIView.as_view(queryset=Broker.objects.all(), serializer_class=BrokerSerializer),
        name='broker_list'),

]

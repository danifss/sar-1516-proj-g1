from django.conf.urls import include, url
from api import views
from rest_framework.generics import ListCreateAPIView, ListAPIView
# from core.models import Service, Broker
# from serializers import ServiceSerializer


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),


    # url(r'^services/$', ListCreateAPIView.as_view(queryset=Service.objects.all(), serializer_class=ServiceSerializer),
    #     name='services-list'),

    # ex: api/services/
    url(r'^services/$', views.listCreateService.as_view(), name='services-list-create'),

    # ex: api/services/id/1/
    url(r'^services/id/(?P<pk>[0-9]+)/$', views.ServiceById.as_view(), name='services-del'),

    # ex: api/services/daniel/
    url(r'^services/(?P<nickname>[a-zA-z0-9]+)/$', views.ServiceByNickname.as_view(), name='service-nickname'),

    # ex: api/services/10.0.0.20/22/
    url(r'^services/(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})/(?P<port>\d+)/$', views.ServiceByIpPort.as_view(),
        name='services-ip-port'),

    # ex: api/brokers/
    # url(r'^brokers/$', ListAPIView.as_view(queryset=Broker.objects.all(), serializer_class=BrokerSerializer),
    #     name='broker_list'),

]

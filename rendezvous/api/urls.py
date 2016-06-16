from django.conf.urls import include, url
from api import views
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView
from core.models import Service
from serializers import ServiceSerializer


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # ex: api/services/
    url(r'^services/$', ListCreateAPIView.as_view(queryset=Service.objects.all(), serializer_class=ServiceSerializer),
        name='services-list'),

    # ex: api/services/1/
    # url(r'^services/del/(?P<pk>[0-9]+)/$', DestroyAPIView.as_view(queryset=Service.objects.all(),
    #                                                               serializer_class=ServiceSerializer),
    #     name='services-del'),
    url(r'^services/del/(?P<pk>[0-9]+)/$', views.delServiceById.as_view(), name='services-del'),

    # ex: api/services/10.0.0.20/22/
    url(r'^services/del/(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})/(?P<port>\d+)/$', views.delServiceByIpPort.as_view(),
        name='services-del'),

]

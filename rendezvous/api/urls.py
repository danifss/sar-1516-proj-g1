from django.conf.urls import include, url
from api import views
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),


]

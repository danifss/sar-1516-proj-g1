from django.conf.urls import include, url
from api import views

urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # ex: api/services/
    url(r'^services/$', views.ServicesList.as_view()),
]

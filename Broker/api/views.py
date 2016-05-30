from rest_framework import generics
from core.models import User, Service, Broker
from core.serializers import UserSerializer, ServiceSerializer, BrokerSerializer
from httplib import HTTPResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Returns a list of available services in the networks
# class ServicesList(APIView):
#     """<b>List Services</b>"""
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     allowed_methods = ['get']
#
#     def get(self, request):
#         """
#         Gets a list of services existing in the network
#
#
#
#         <b>Details</b>
#
#         METHODS : GET
#
#
#
#         <b>RETURNS:</b>
#
#         - 200 OK.
#
#         - 400 BAD REQUEST
#         #         """
#
#         # X-CSRFToken: UHO29TxPYCyqUcKqcNQeK5kF8BG0p7lX
#         print(request.META['CSRF_COOKIE'])
#
#         try:
#             services = Service.objects.all()
#             resp = []
#             for s in services:
#                 resp += [s]
#             self.queryset = resp
#         except:
#             self.queryset = []
#
#         return Response(status=status.HTTP_200_OK, data={'data': str(self.queryset)})

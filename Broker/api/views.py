from rest_framework import generics
from core.models import User, Service, Broker
from core.serializers import UserSerializer, ServiceSerializer, BrokerSerializer
from httplib import HTTPResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import requests

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

@api_view(['GET'])
def connect(request, path=None):
    print(request.data)


    r = requests.get(path)
    requests.post(path, data=request.data)
    data = (r.text)

    return Response(status=status.HTTP_200_OK, data=data)


class delServiceByIpPort(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    allowed_methods = ['delete']

    def delete(self, request, ip=None, port=None):  # ip1=None, ip2=None, ip3=None, ip4=None, port=None):
        """
        Deletes a service by given ip and port



        <b>Details</b>

        METHODS : DELETE



        <b>RETURNS:</b>

        - 200 OK.

        - 404 NOT FOUND

        - 400 BAD REQUEST
        """
        #         # X-CSRFToken: UHO29TxPYCyqUcKqcNQeK5kF8BG0p7lX
        #         print(request.META['CSRF_COOKIE'])

        try:
            if ip is not None and port is not None:
                service = Service.objects.get(ip=ip, port=port)
                service.delete()
                return Response(status=status.HTTP_200_OK, data={"detail": "Service deleted with success."})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Bad request."})


# from rest_framework import generics
# from core.models import User, Service, Broker
# from serializers import UserSerializer, ServiceSerializer, BrokerSerializer
# from httplib import HTTPResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

import requests
from requests import exceptions


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

host = 'http://10.1.1.2:9000/'


class listCreateService(APIView):
    # queryset = Service.objects.all()
    # serializer_class = ServiceSerializer
    allowed_methods = ['get', 'post']

    def get(self, request):
        """
            Gets every Services




            <b>Details</b>

            METHODS : GET



            <b>RETURNS:</b>

            - 200 OK

            - 400 BAD REQUEST

            - 404 NOT FOUND

            ---
            omit_parameters:
            - form
        """
        try:
            url = host + 'api/services/'
            result = proxy(path=url, method='GET')
            if result.status_code == 200:
                return Response(status=status.HTTP_200_OK, data=result.data)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Bad request."})
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})

    @csrf_exempt
    def post(self, request):
        """
        Creates a new Service




        <b>Details</b>

        METHODS : POST




        <b>Example:</b>


        {

            "name": "Chat em silva-pc",

            "description": "Chat cliente para conversa",

            "ip": "10.0.0.10",

            "port": "12345"

        }



        <b>RETURNS:</b>

        - 200 OK.

        - 400 BAD REQUEST


        ---
        omit_parameters:
            - form
        """
        # X-CSRFToken: UHO29TxPYCyqUcKqcNQeK5kF8BG0p7lX
        # print(request.META['CSRF_COOKIE'])
        try:
            url = host + 'api/services/'
            result = proxy(path=url, method='POST', data=request.data)
            if 200 <= result.status_code <= 250:
                return Response(status=status.HTTP_200_OK, data=result.data)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Bad request."})
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=result.data) # {"detail": "Internal Server Error."}


class delServiceByIpPort(APIView):
    # queryset = Service.objects.all()
    # serializer_class = ServiceSerializer
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
                url = host + 'api/services/del/' + str(ip) + '/' + str(port) + '/'
                result = proxy(path=url, method='DELETE')
                if result.status_code == 200:
                    return Response(status=status.HTTP_200_OK, data={"detail": "Service deleted with success."})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Bad request."})

        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})


class delServiceById(APIView):
    # queryset = Service.objects.all()
    # serializer_class = ServiceSerializer
    allowed_methods = ['delete']

    def delete(self, request, pk=None):
        """
        Deletes a service by given id



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
            id = int(pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Bad request."})

        try:
            url = host + 'api/services/del/' + str(id) + '/'
            result = proxy(path=url, method='DELETE')
            if result.status_code == 200:
                return Response(status=status.HTTP_200_OK, data=result.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})

        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})


def proxy(path=None, method='GET', data=None):
    timeout = 60 * 5

    r = None
    # 501 Not Implemented
    response = Response({'detail': '501 Not Implemented'}, 501)
    try:
        if method == 'GET':
            r = requests.get(path, data=data, timeout=timeout)
        elif method == 'POST':
            r = requests.post(path, data=data, timeout=timeout)
        elif method == 'PUT':
            r = requests.put(path, data=data, timeout=timeout)
        elif method == 'DELETE':
            r = requests.delete(path, data=data, timeout=timeout)

    except exceptions.Timeout:
        # 504 Gateway Timeout
        response = Response({'detail': '504 Gateway Timeout'}, 504)
    except exceptions.ConnectionError:
        # 503 Service Unavailable
        response = Response({'detail': '503 Service Unavailable'}, 503)

    if r is not None:
        if r.headers.get('Content-Type', None) == 'application/json':
            response = Response(r.json(), r.status_code)
        else:
            response = Response(r.text, r.status_code)
    return response


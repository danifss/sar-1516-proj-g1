from django.shortcuts import render
from rest_framework import generics
from core.models import User, Service
from serializers import UserSerializer, ServiceSerializer
from httplib import HTTPResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class sericeById(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    allowed_methods = ['get']

    def get(self, request, pk=None):
        """
        Gets Service by given id




        <b>Details</b>

        METHODS : GET



        <b>RETURNS:</b>

        - 200 OK

        - 404 NOT FOUND

        ---
        omit_parameters:
        - form
        """
        try:
            int_pk = int(pk)
            result = Service.objects.get(serviceID=int_pk)
            data = {
                "serviceID": result.serviceID,
                "name": result.name,
                "description": result.description,
                "ip": result.ip,
                "port": result.port,
                "createdOn": result.createdOn,
            }
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})



class delServiceByIpPort(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    allowed_methods = ['delete']

    def delete(self, request, ip=None, port=None):
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


class delServiceById(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
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
            service = Service.objects.get(serviceID=id)
            service.delete()
            return Response(status=status.HTTP_200_OK, data={"detail": "Service deleted with success."})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Service not found."})

from rest_framework import generics
from core.models import User
from core.serializers import UserSerializer
from httplib import HTTPResponse
from rest_framework.response import Response
from rest_framework import status


# Returns a list of available services in the networks
class ServicesList(generics.ListCreateAPIView):

    """<b>User Login</b>"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    allowed_methods = ['get']

    def get(self, request):
        """
        Gets user id if credentials are correct



        <b>Details</b>

        METHODS : GET



        <b>RETURNS:</b>

        - 200 OK.

        - 400 BAD REQUEST
        #         """
        if 'password' in request.GET and 'email' in request.GET:
            try:
                user = User.objects.get(email__iexact=request.GET.get('email'))
                if user.check_password(request.GET.get('password')):
                    return Response(status=status.HTTP_200_OK, data={'id': user.id, 'first_name': user.first_name,
                                                                     'last_name': user.last_name})
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class UserLogin(generics.ListCreateAPIView):
#     """<b>User Login</b>"""
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     allowed_methods = ['get']
#
#     def get(self, request):
#         """
#         Gets user id if credentials are correct
#
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
#
#         email -- registration email
#         password -- registration password
#         ---
#         omit_parameters:
#         - form
#         """
#         if 'password' in request.GET and 'email' in request.GET:
#             try:
#                 user = CustomUser.objects.get(email__iexact = request.GET.get('email'))
#                 if user.check_password(request.GET.get('password')):
#                     return Response(status=status.HTTP_200_OK, data={'id': user.id, 'first_name': user.first_name,
#                                                                      'last_name': user.last_name})
#                 else:
#                     return Response(status=status.HTTP_400_BAD_REQUEST)
#             except:
#                 pass
#         return Response(status=status.HTTP_400_BAD_REQUEST)

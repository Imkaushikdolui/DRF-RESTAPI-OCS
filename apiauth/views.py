from django.utils import timezone
from rest_framework import generics
from apiauth.models import Account
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .email import send_otp
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
# Create your views here.

# JWT authentication


User = get_user_model()

class AccountLoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        # httponly = true //becuase we dont want frontend to acess the token,its for the backend only
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            "jwt": token,
        }

        return response


account_login_view = AccountLoginAPI.as_view()


class UserJWTView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("UnAuthenticated!!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Token is invalid")

        # Use single quotes around 'id' to access the key
        user_id = payload['id']
        user = User.objects.get(id=user_id)
        serializer = AccountSerializer(user)
        return Response(serializer.data)


user_jwt_view = UserJWTView.as_view()


class AccountLogoutAPI(APIView):
    def post(self, request):

        response = Response({"message": "Logged out successfully"})

        # Delete the 'jwt' cookie by setting its value to an empty string and setting its expiration time to a past date
        response.delete_cookie('jwt')

        return response


account_logout_view = AccountLogoutAPI.as_view()

# ACCOUNT REGISTER APIViews


class AccountRegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = AccountSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'Registration successful check your email!!!',
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': 'Registration failed something went wrong!!',
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)


account_register_view = AccountRegisterAPI.as_view()


class VerifyOTP(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = Account.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'something went wrong!!',
                        'data': 'invalid email'
                    })
                if not user.first().otp == otp:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong!!',
                        'data': 'wrong otp'
                    })
                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Account verified !!!',
                    'data': {}
                })

            return Response({
                'status': 400,
                'message': 'Registration failed something went wrong!!',
                'data': serializer.errors,
            })

        except Exception as e:
            print(e)


account_verify_view = VerifyOTP.as_view()


class AccountListAPIView(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        # Filter the queryset to retrieve only verified accounts
        queryset = Account.objects.filter(is_verified=True)

        # Check if 24 hours have passed since the registration
        time_threshold = timezone.now() - timezone.timedelta(hours=24)

        # Delete unverified accounts older than 24 hours
        Account.objects.filter(
            is_verified=False, date_joined__lte=time_threshold).delete()

        return queryset


account_list_view = AccountListAPIView.as_view()


class AccountDetailAPIView(generics.RetrieveAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


account_detail_view = AccountDetailAPIView.as_view()


class AccountUpdateAPIView(generics.UpdateAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()


account_update_view = AccountUpdateAPIView.as_view()


class AccountDestroyAPIView(generics.DestroyAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()


account_destroy_view = AccountDestroyAPIView.as_view()

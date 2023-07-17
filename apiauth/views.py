from django.utils import timezone
from rest_framework import generics
from apiauth.models import Account
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .email import send_otp
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
# Create your views here.

# JWT authentication


User = get_user_model()

class AccountLoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                
                # Check if the user exists with the given email
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = None

                # Authenticate the user based on email and password
                if user is not None and user.check_password(password):
                    if not user.is_verified:
                        return Response({
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'Your Account is not verified',
                            'data': {}
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email or password',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid request',
                'data': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal server error',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
account_login_view = AccountLoginAPI.as_view()


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
        Account.objects.filter(is_verified=False, date_joined__lte=time_threshold).delete()

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

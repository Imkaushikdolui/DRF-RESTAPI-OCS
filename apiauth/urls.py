from django.urls import path
from .views import *

urlpatterns = [
    
    # account register endpoint
    path('register/',account_register_view,name='account-register'),
    path('verify/',account_verify_view,name='account-register'),
    
    # account jwt and login endpoint
    path('login/',account_login_view,name='account-login'),
    path('userjwt/',user_jwt_view,name='user-jwt'),
    path('logout/',account_logout_view,name='account-logout'),
    

    # account endpoints
    path('account/', account_list_view, name='account-list'),
    path('account/<int:pk>/', account_detail_view, name='account-detail'),
    path('account/<int:pk>/update/', account_update_view, name='account-update'),
    path('account/<int:pk>/delete/', account_destroy_view, name='account-delete'),
]

from django.urls import path
from .views import user_registration, verify_otp, user_login, logout_user, admin_dashboard

urlpatterns = [
    path('register/', user_registration, name='register'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]

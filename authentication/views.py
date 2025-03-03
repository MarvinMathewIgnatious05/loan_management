import random
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser  # Import custom permission

User = get_user_model()

@api_view(['POST'])
def user_registration(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'User')  # Default to 'User'

    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    otp = str(random.randint(100000, 999999))  # Generate OTP as string

    user = User.objects.create_user(username=username, email=email, password=password, role=role, is_verified=False)
    user.otp = otp
    user.save()

    send_mail(
        "Your OTP Code",
        f"Your OTP is {otp}",
        "noreply@example.com",
        [email],
        fail_silently=False,
    )

    return Response({'message': 'User registered. Verify OTP to activate account.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    try:
        user = User.objects.get(email=email)

        if user.otp != otp:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.otp = None  # Clear OTP after verification
        user.save()

        return Response({'message': 'OTP verified successfully. You can now login.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_verified:
        return Response({'message': 'Please verify your OTP first'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=user.username, password=password)  # Authenticate using username

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role
        }, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the refresh token
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Apply authentication & role-based access
def admin_dashboard(request):
    return Response({'message': 'Welcome, Admin!'}, status=status.HTTP_200_OK)

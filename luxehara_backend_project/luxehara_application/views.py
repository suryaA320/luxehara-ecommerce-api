from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from luxehara_application.models import *
from luxehara_application.serializers import *
from rest_framework.permissions import IsAuthenticated
from Custom_Authentication import CookieJWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, logout

# Create your views here.
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token


        response_data = {
            "user": UserSerializer(user).data,
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # Set HttpOnly Cookies
        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=1800
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=86400
        )
        return response

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the token
            except Exception:
                pass  # Ignore if token is already invalid

        logout(request)
        response = Response({"message": "Logged out successfully"}, status=200)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token not found"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)  # This automatically validates the token

            # Generate new access token
            access_token = refresh.access_token

            response = Response({"message": "Token refreshed"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=str(access_token),
                httponly=True,
                secure=False,   # Set to True in production
                samesite="Lax",
                max_age=1800,
            )
            return response

        except TokenError:  # Handles expired or invalid token
            response = Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie("refresh_token")
            response.delete_cookie("access_token")
            return response
        
        
class RegisterView(APIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT Tokens
            refresh = RefreshToken.for_user(user)

            response = Response(
                {
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

            # Set tokens in HTTP-only cookies
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=False,  # Change to True in production (HTTPS required)
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import (UserSerializer,LoginSerializer)
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import logging
# Create your views here.


logger = logging.getLogger('Apps.Users')

class RegisterView(GenericAPIView):
    serializer_class=UserSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response={
                "status":status.HTTP_201_CREATED,
                "message":"User Registered Successfully"
            }
            return Response(response,status=status.HTTP_201_CREATED)
        except Exception:
            logger.error(f"An error occurred during Registration: {str(e)}")
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"User Registered Failed",
                "errors":serializer.errors
            }
            return Response(response)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(serializer.errors)
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Login Failed",
                "errors": serializer.errors
            },status.HTTP_400_BAD_REQUEST,)
        try:
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username,password=password)
            if user:
                token_serializer=TokenObtainPairSerializer(data=request.data)
                if token_serializer.is_valid(raise_exception=True):
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Login Successfully",
                        "data": token_serializer.validated_data
                    }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return Response({
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Login Failed",
                    "errors": "Invalid username or password."
                },status.HTTP_401_UNAUTHORIZED,)
        except Exception as e:
            logger.error(f"An error occurred during login: {str(e)}")
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Login Failed",
                "errors": "An unexpected error occurred."
            },status.HTTP_500_INTERNAL_SERVER_ERROR,)




class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token',None)
        try:
            if refresh_token is None:
                raise ValidationError("Refresh token is required for logout.")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.username} logged out successfully.")
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Logout Successful",
            })

        except Exception as e:
           
            logger.error(f"Error during logout: {str(e)}")
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Logout Failed",
                "errors": str(e),
            })

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework import status
from .models import UserProfile

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create an empty profile for the user
            UserProfile.objects.create(user=user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username_or_email']
            password = serializer.validated_data['password']

            # Check if the username_or_email is an email
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                    username = user.username
                except User.DoesNotExist:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                username = username_or_email

            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

logger = logging.getLogger(__name__)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Try to get the user's profile
            profile = request.user.profile
            serializer = UserProfileSerializer(profile)
            
            # Log the profile fields
            logger.info(f"Retrieved profile: {profile.__dict__}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            # If the profile does not exist, inform the user
            return Response({"error": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other unexpected errors
            logger.error(f"Error retrieving profile: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Try to get or create the user's profile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Log the profile fields
            logger.info(f"Updating/creating profile: {profile.__dict__}")

            # If the profile is found or newly created, update the data
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Log the updated profile data
                logger.info(f"Profile saved: {serializer.data}")

                if created:
                    return Response({"message": "Profile created successfully", "profile": serializer.data}, status=status.HTTP_201_CREATED)
                return Response({"message": "Profile updated successfully", "profile": serializer.data}, status=status.HTTP_200_OK)
            else:
                # Log validation errors
                logger.error(f"Profile validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Error updating/creating profile: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import UserLocation
from django.contrib.auth.models import User

class UserLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        city = request.data.get('city')

        if not city:
            return Response({"error": "City is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Update or create the location for the user based on city
            location, created = UserLocation.objects.update_or_create(
                user=user,
                defaults={'city': city}
            )
            print(f"User: {user.username}, City: {city}")  # Debugging line
            return Response({"message": "Location updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MatchingUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Get the user's current city
            user_location = UserLocation.objects.get(user=user)
            city = user_location.city

            # Debugging: Print the current user and city
            print(f"Current User: {user.username}, City: {city}")

            # Find all users in the same city
            matching_users = UserLocation.objects.filter(city=city).exclude(user=user)
            user_data = [{"username": loc.user.username, "city": loc.city} for loc in matching_users]

            # Debugging: Print the matching users
            print(f"Matching Users: {user_data}")

            return Response(user_data, status=status.HTTP_200_OK)
        except UserLocation.DoesNotExist:
            return Response({"error": "User location not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

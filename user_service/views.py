from rest_framework import viewsets, permissions, status, generics
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from user_service.models import InstructorProfile, StudentProfile
from user_service.serializers import (
    UserSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer, 
    ChangePasswordSerializer, ConfirmEmailSerializer, StudentProfileSerializer, InstructorProfileSerializer
)

from common import permissions as custom_permissions
User = get_user_model()

# Create your views here.

class ConfirmEmailView(APIView):

    queryset = get_user_model().objects.all()
    serializer_class = ConfirmEmailSerializer
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"error": "Invalid user ID"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Invalid token"}, status=400)

class ChangePasswordView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = request.data.get("old_password")
        if not request.user.check_password(old_password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class CustomTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Define a get_queryset method that returns only active users for non-superusers
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(is_active=True)

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'destroy':
            return {permissions.IsAuthenticated(), permissions.IsAdminUser()}
        return super().get_permissions()
    

class StudentProfileViewset(viewsets.ModelViewSet):

    """
    list: Get all user profiles. Search by "first_name", "last_name", "email".
    retrieve: Get a single profile by profile ID.
    partial_update: Update profile by profile ID.
    """

    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user__is_active=True)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [
                permissions.IsAuthenticated(),
                custom_permissions.IsOwnerOrReadOnly(),
            ]
        return super().get_permissions()


class InstructorProfileViewset(viewsets.ModelViewSet):

    """
    list: Get all user profiles. Search by "first_name", "last_name", "email".
    retrieve: Get a single profile by profile ID.
    partial_update: Update profile by profile ID.
    """

    serializer_class = InstructorProfileSerializer
    queryset = InstructorProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user__is_active=True)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [
                permissions.IsAuthenticated(),
                custom_permissions.IsOwnerOrReadOnly(),
            ]
        return super().get_permissions()

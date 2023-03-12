from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from user_service.serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()

# Create your views here.

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


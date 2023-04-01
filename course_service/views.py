from django.shortcuts import render
from rest_framework import viewsets, permissions, validators, generics
from common import permissions as custom_permissions
from .models import Course 
from user_service.models import InstructorProfile
from django.contrib.auth import get_user_model
from .serializers import CourseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import CourseFilter
from .pagination import CustomPagination
from .renderers import CustomRenderer

User = get_user_model()
# Create your views here.

class CourseViewSet(AutoPrefetchViewSetMixin,viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    search_fields = ["name", "instructor__user__first_name", "instructor__user__last_name"]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["reviews", "price"]
    filterset_class = CourseFilter
    pagination_class = CustomPagination 
    renderer_classes = [CustomRenderer]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(instructor__user__is_active=True)
    
    def get_permissions(self):
        
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]  
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [custom_permissions.IsInstructorOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
            
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # Assign users with is_instructor field to create courses
        if not self.request.user.is_instructor:
            raise validators.ValidationError(
                                                {
                                                "status": "Error",
                                                "message": "User must have is_instructor = True to create a course"
                                                }
                                            )
        instructor_profile = InstructorProfile.objects.filter(user=self.request.user).first()
        serializer.save(instructor=instructor_profile) 


        
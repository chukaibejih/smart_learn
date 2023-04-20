from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, serializers, filters
from rest_framework.filters import OrderingFilter, SearchFilter

from common import permissions as custom_permissions
from user_service.models import InstructorProfile
from .models import Course, Review,InstructorSkill, Module, Tag, TagModule
from .serializers import CourseSerializer, ReviewSerializer, InstructorSkillSerializer, ModuleSerializer, TagSerializer, TagModuleSerializer
from .filters import CourseFilter
from .pagination import CustomPagination
from .renderers import CustomRenderer
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import validators

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
            self.permission_classes = [custom_permissions.IsCreatorOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
            
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # Assign users with is_instructor field to create courses
        if not self.request.user.is_instructor:
            raise validators.ValidationError(
                                            {
                                            "detail": "User must have is_instructor = True to create a course"
                                            }
                                            )
        instructor_profile = get_object_or_404(InstructorProfile, user=self.request.user)
        serializer.save(instructor=instructor_profile) 


class ModuleView(viewsets.ModelViewSet):
    # Set the queryset and serializer_class
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        # Get the course id and module id from the URL parameter
        course_id = self.kwargs.get('course_pk')
        module_id = self.kwargs.get('pk')

        # If we have both course id and module id from the URL parameter, let's get that particular module from that particular course
        if course_id and module_id:
            queryset = Module.objects.filter(course=course_id, id=module_id)
        # If we have only course id, let's get all the modules belonging to that course
        elif course_id:
            queryset = Module.objects.filter(course=course_id)
        # If we have no parameters, then let's get all the modules irrespective of the course they belong to
        else:
            queryset = Module.objects.all()

        # If the user is staff, return all the modules
        if self.request.user.is_staff:
            return queryset
        # Otherwise, return only the modules whose course instructor is active
        return queryset.filter(course__instructor__user__is_active=True)

    def get_permissions(self):
        # Set the permission_classes based on the action
        permission_classes = [permissions.IsAuthenticated, custom_permissions.IsCourseInstructor]
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Set the course instructor to the current authenticated user
        course_instructor = self.request.user.instructor_profile
        course = serializer.validated_data['course']

        # Check if the course instructor is creating the module for their own course
        if course.instructor != course_instructor:
             raise serializers.ValidationError("You can only create modules for courses that you are an instructor of.")

        # Save the module
        serializer.save()



class TagView(viewsets.ModelViewSet):
    # Set the queryset and serializer_class
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagModuleView(viewsets.ModelViewSet):
    # Set the queryset and serializer_class
    queryset = TagModule.objects.all()
    serializer_class = TagModuleSerializer



class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    renderer_classes = [CustomRenderer]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    
    def perform_create(self, serializer):
        # Ensure a user makes only ony one review per course
        try:
            course_identity = self.kwargs["pk"]
            course = get_object_or_404(Course, id=course_identity)
            serializer.save(course=course, user=self.request.user)
        except IntegrityError:
            raise validators.ValidationError(
                                            {
                                            "detail": "This user has already created a review about this course"
                                            }
                                            )
            
            
class ReviewListView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = ReviewSerializer 
    pagination_class = CustomPagination 
    renderer_classes = [CustomRenderer]
    queryset = Review.objects.all()
    permission_classes = [custom_permissions.IsCreatorOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return super().get_queryset().filter(user__is_active=True, course__id=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer 
    renderer_classes = [CustomRenderer]
    permission_classes = [custom_permissions.IsCreatorOrReadOnly]
    
    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(Review, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj 

class InstructorSkillCreateView(generics.CreateAPIView):
    serializer_class = InstructorSkillSerializer
    permission_classes = [custom_permissions.IsCreatorOrReadOnly]
    renderer_classes = [CustomRenderer]
    queryset = InstructorSkill.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_instructor:
            raise validators.ValidationError(
                                            {
                                            "detail": "User must have is_instructor = True to create a course"
                                            }
                                            )
        instructor_profile = get_object_or_404(InstructorProfile, user=self.request.user)
        serializer.save(instructor=instructor_profile)

class InstructorSkillListView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = InstructorSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomRenderer]
    pagination_classes = CustomPagination
    queryset = InstructorSkill.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(instructor__user__is_active=True)


class InstructorSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorSkillSerializer
    permission_classes = [custom_permissions.IsCreatorOrReadOnly]
    renderer_classes = [CustomRenderer]

    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(Review, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj









    
    
    
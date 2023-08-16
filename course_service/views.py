from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    permissions,
    generics,
    serializers,
    validators,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from common import permissions as custom_permissions
from user_service.models import InstructorProfile
from .models import (
    Course,
    Review,
    Module,
    Lesson,
    Tag,
    TagModule,
    Quiz
)
from .serializers import (
    CourseSerializer,
    ReviewSerializer,
    LessonSerializer,
    ModuleSerializer,
    TagSerializer,
    TagModuleSerializer,
    QuizSerializer
)
from .filters import CourseFilter
from common.pagination import CustomPagination
from .renderers import CustomRenderer
from django_auto_prefetching import AutoPrefetchViewSetMixin

User = get_user_model()


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


class ModuleView(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    # Set the queryset and serializer_class
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = CustomPagination 
    renderer_classes = [CustomRenderer]

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
             raise serializers.ValidationError({"detail: " : "You can only create modules for courses that you are an instructor of."})

        # Save the module
        serializer.save()


class LessonView(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    # set the queryset and serializer class
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination 
    renderer_classes = [CustomRenderer]

    # Get the module id and lesson id from the URL parameter
    def get_queryset(self):
        module_id = self.kwargs.get('module_pk')
        lesson_id = self.kwargs.get('pk')

        # if we have both module id and lesson id, get the particular lesson of a particular module
        if module_id and lesson_id:
            queryset = Lesson.objects.filter(module=module_id, id=lesson_id)

        # if we have only module id, get all the lessons of that perticular module
        elif module_id:
            queryset = Lesson.objects.filter(module=module_id)
        else:
            queryset = Module.objects.all()
    
        # if the user is a staff, return all lesson
        if self.request.user.is_staff:
            return queryset
        # Otherwise, return only the lessons whose course instructor is active
        return queryset.filter(module__course__instructor__user__is_active=True)

    def get_permissions(self):
        # Set the permission_classes based on the action
        permission_classes = [permissions.IsAuthenticated, custom_permissions.IsCourseInstructor]
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):

        if not self.request.user.is_instructor:
            raise validators.ValidationError(
                                            {
                                            "detail": "User must instructor to create a course"
                                            }
                                            )
        
        # Set the course instructor to the current authenticated user
        course_instructor = self.request.user.instructor_profile
        module = serializer.validated_data['module']
        course = module.course

        # Check if the course instructor is creating the module for their own course
        if course.instructor != course_instructor:
             raise serializers.ValidationError("You cannot create a new lesson for a module that belongs to a course you are not an instructor of.")

        # Save the module
        serializer.save()


class TagView(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    # Set the queryset and serializer_class
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    renderer_classes = [CustomRenderer]
    permission_classes = [permissions.IsAuthenticated]


class TagModuleView(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    # Set the queryset and serializer_class
    queryset = TagModule.objects.all()
    serializer_class = TagModuleSerializer
    renderer_classes = [CustomRenderer]
    permission_classes = [permissions.IsAuthenticated]


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
            course.reviews += 1
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


class QuizView(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    pagination_class = CustomPagination 
    renderer_classes = [CustomRenderer]
    permission_classes = []
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]  
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [custom_permissions.IsCreatorOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
            
        return super().get_permissions()
    
    def get_queryset(self):
        lesson_id = self.kwargs["lesson_pk"]
        if self.request.user.is_staff:
            return super().get_queryset()
        
        if lesson_id:
            return super().get_queryset().filter(  
                                                 lesson=lesson_id, 
                                                 lesson__module__course__instructor__user__is_active=True
                                                )
        return super().get_queryset().none()
            
    def perform_create(self, serializer):
        instructor = get_object_or_404(InstructorProfile, user=self.request.user)
        lesson = get_object_or_404(Lesson, module__course__instructor=instructor)

        if not self.request.user.is_instructor:
            raise validators.ValidationError(
                                            {
                                            "detail": "User must have is_instructor = True to create a certificate"        
                                            }
                                            )
        serializer.save(lesson=lesson)
    
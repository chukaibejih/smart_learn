from rest_framework import viewsets, permissions, generics, serializers
from .models import Tag, TagModule, Module
from .serializers import TagSerializer, TagModuleSerializer, ModuleSerializer
from common import permissions as custom_permissions

# Create your views here.


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagModuleView(viewsets.ModelViewSet):
    queryset = TagModule.objects.all()
    serializer_class = TagModuleSerializer


class ModuleView(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(course__instructor__user__is_active=True)
    
    def get_permissions(self):

        if self.action in ['list', 'retrive']:
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated, custom_permissions.IsCourseInstructor]
        
        # returns a list of permission instances based on the classes defined in permission_classes.
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # set the course instuctor to the current authenticated user
        
        course_instructor = self.request.user.instructor_profile
        course = serializer.validated_data['course']

        if course.instructor != course_instructor:
             raise serializers.ValidationError("You can only create modules for courses that you are an instructor of.")
        serializer.save()
    
    


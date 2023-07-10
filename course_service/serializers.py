from .models import (
 Course, 
 Review, 
 Module, 
 Lesson, 
 Tag, 
 TagModule, 
 Quiz
 )
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    
    instructor_name = serializers.SerializerMethodField()

    def get_instructor_name(self, obj):
        return obj.get_instructor_fullname

    class Meta:
        model = Course 
        fields = "__all__"
        read_only_fields = ("reviews", "instructor")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class TagModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModule
        fields = "__all__"
        

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"        

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Review 
        fields = "__all__"

        
class QuizSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField()
    
    class Meta:
        model = Quiz 
        fields = "__all__"

from .models import Course, Review, Module, Lesson, Tag, TagModule, InstructorSkill, SkillCertification
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    
    instructor_name = serializers.SerializerMethodField()

    def get_instructor_name(self, obj):
        return obj.get_instructor_fullname

    class Meta:
        model = Course 
        fields = "__all__"


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


class InstructorSkillSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()
    
    class Meta:
        model = InstructorSkill
        fields = "__all__"

class SkillCertificationSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    
    def get_instructor(self, obj):
        return obj.skill.instructor.user.email  
    
    class Meta:
        model = SkillCertification
        fields = "__all__"
        

        
        

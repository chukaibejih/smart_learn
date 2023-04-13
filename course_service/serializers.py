from .models import Course, Review
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    
    instructor_name = serializers.SerializerMethodField()

    def get_instructor_name(self, obj):
        return obj.get_instructor_fullname

    class Meta:
        model = Course 
        fields = "__all__"
        

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Review 
        fields = "__all__"
        

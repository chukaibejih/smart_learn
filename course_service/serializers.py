from .models import Course 
from rest_framework import serializers 


class CourseSerializer(serializers.ModelSerializer):
    
    instructor_name = serializers.SerializerMethodField()
    
    def get_instructor_name(self, obj):
        return obj.get_instructor_fullname
    
    class Meta:
        model = Course 
        fields = "__all__"
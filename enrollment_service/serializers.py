from rest_framework import serializers
from course_service.models import Course
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class EnrollmentByCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='student.user.first_name')
    email = serializers.EmailField(source='student.user.email')

    class Meta:
        model = Enrollment
        fields = ['name', 'email', 'enrollment_date']


class StripeSerializer(serializers.Serializer):
    course = serializers.CharField()

    def validate_course(self, value):
        try:
            course = Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")
        return course.id

    def create(self, validated_data):
        return validated_data

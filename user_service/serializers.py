from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import RegexValidator, MaxValueValidator, MinValueValidator
from user_service.models import User, StudentProfile, InstructorProfile, SMSCode


class ConfirmEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['token', 'uidb64']
        
class ConfirmSmsSerializer(serializers.ModelSerializer):
     number = serializers.CharField(max_length=6, required=True,

                                    validators=[RegexValidator(r'^\d{6}$'),

                                                MinaValueValidator(999999),

                                                MaxValueValidator(100000)])
        
      class Meta:
        model = SMSCode
        fields = ['number']
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 

    """Override default token login to include user data"""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verified:
            raise serializers.ValidationError({"error":"Email is not verified."})

        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "is_instructor": self.user.is_instructor,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
                "is_verified": self.user.is_verified
            }
        )

        return data
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type':'password'})

    # Meta class to specify the model and its fields to be serialized
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password','is_instructor', ] 

    # Method to validate the email entered by the user
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value
    
    # Method to validate the password entered by the user
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    # Create a new user object using the validated data
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_instructor=validated_data['is_instructor'],
            is_verified=False

        )
        return user
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_instructor', 'is_active', 'is_verified', 'created_at',]


class StudentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile
        fields = "__all__"
     

class InstructorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstructorProfile
        fields = "__all__"


class RetrieveUserSerializer(serializers.ModelSerializer):
    student_profile = serializers.SerializerMethodField()
    instructor_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_instructor', 'is_active', 'is_verified', 'created_at', 'student_profile', 'instructor_profile']

    def get_student_profile(self, obj):
        try:
            profile = obj.student_profile
            return StudentProfileSerializer(profile).data
        except StudentProfile.DoesNotExist:
            return None

    def get_instructor_profile(self, obj):
        try:
            profile = obj.instructor_profile
            return InstructorProfileSerializer(profile).data
        except InstructorProfile.DoesNotExist:
            return None

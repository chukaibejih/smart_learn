from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from user_service.models import InstructorSkill, SkillCertification, User, StudentProfile, InstructorProfile, SMSCode


class ConfirmEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['token', 'uidb64']
        
class ConfirmSmsSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=6, required=True,
                                    validators=[MinValueValidator(100000),
                                                MaxValueValidator(999999)])
    def validate_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Number must be a string of digits.")
  
        # Retrieve the SMSCode instance for the authenticated user
        sms_code = SMSCode.objects.filter(user=self.context['request'].user).first()
        if not sms_code:
            raise serializers.ValidationError("No SMS verification code found for this user.")
        
        # Compare the user-provided number with the number in the SMSCode instance
        if value != sms_code.number:
            raise serializers.ValidationError("Incorrect SMS verification code.")
        
        return value
        
    class Meta:
        model = SMSCode
        fields = ['number']
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        # Validate the password meets strength requirements
        validate_password(value)
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        # Check if the old password matches the current password of the user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password does not match.")
        return value
    
    def validate(self, data):
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)

        if old_password and new_password and old_password == new_password:
            raise serializers.ValidationError("New password cannot be the same as old password.")

        return data

    
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
        exclude = ['user']

class StudentPublicProfileSerializer(StudentProfileSerializer):
    """ Child class that inherit from it's parents and changing Meta class properities """
    class Meta(StudentProfileSerializer.Meta):
        exclude = [
            "date_of_birth","phone_number",
            "address","city","state","country"
        ]


class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        exclude = ['user']

class InstructorPublicProfileSerializer(InstructorProfileSerializer):
    """ Child class that inherit from it's parents and changing Meta class properities """
    class Meta(InstructorProfileSerializer.Meta):
        exclude = [
            "date_of_birth","phone_number",
            "address","city","state","country"
        ]

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
        
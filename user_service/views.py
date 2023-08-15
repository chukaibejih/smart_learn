from wsgiref.validate import validator
from django.shortcuts import get_object_or_404
from psycopg2 import IntegrityError
from rest_framework import viewsets, permissions, status, generics
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from course_service.renderers import CustomRenderer
from user_service.models import InstructorSkill, SkillCertification, StudentProfile, InstructorProfile, SMSCode 
from user_service.serializers import (
 InstructorSkillSerializer, SkillCertificationSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer, RetrieveUserSerializer,
    ChangePasswordSerializer, ConfirmEmailSerializer, StudentProfileSerializer, 
    InstructorProfileSerializer, ConfirmSmsSerializer,StudentPublicProfileSerializer,InstructorPublicProfileSerializer
)
from rest_framework import validators


from common.pagination import CustomPagination
from common import permissions as custom_permissions
User = get_user_model()


class SMSCodeView(APIView):

    def get(self, request):

        sms_codes = SMSCode.objects.all()

        serializer = ConfirmSmsSerializer(sms_codes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = ConfirmSmsSerializer(data=request.data)

        if serializer.is_valid():

            number = serializer.validated_data['number']

            try:

                sms_code = SMSCode.objects.get(number=number)

            except SMSCode.DoesNotExist:

                return Response({"error": "SMS code not found"}, status=status.HTTP_404_NOT_FOUND)



            if sms_code.is_expired():

                return Response({"error": "SMS code has expired"}, status=status.HTTP_400_BAD_REQUEST)

            

            return Response({"success": "SMS code confirmed"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ConfirmEmailView(APIView):

    queryset = get_user_model().objects.all()
    serializer_class = ConfirmEmailSerializer
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"error": "Invalid user ID"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Invalid token"}, status=400)
        

class ChangePasswordView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = request.data.get("old_password")
        if not request.user.check_password(old_password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class CustomTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RetrieveUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    # Define a get_queryset method that returns only active users for non-superusers
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        raise PermissionDenied("You do not have permission to access the list of users.")

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action    
    def get_permissions(self):
        if self.action == 'destroy':
            return {permissions.IsAuthenticated(), permissions.IsAdminUser()}
        if self.action == 'create':
            return {permissions.AllowAny()}
        return super().get_permissions()
    

class StudentProfileViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    """
    list: Get all user profiles. Search by "first_name", "last_name", "email".
    retrieve: Get a single profile by profile ID.
    partial_update: Update profile by profile ID.
    """

    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        # return super().get_queryset().filter(user__is_active=True)
        return super().get_queryset().filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [
                permissions.IsAuthenticated(),
                custom_permissions.IsOwnerOrReadOnly(),
            ]
        return super().get_permissions()


class InstructorProfileViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):

    """
    list: Get all user profiles. Search by "first_name", "last_name", "email".
    retrieve: Get a single profile by profile ID.
    partial_update: Update profile by profile ID.
    """

    serializer_class = InstructorProfileSerializer
    queryset = InstructorProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user__is_active=True)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [
                permissions.IsAuthenticated(),
                custom_permissions.IsOwnerOrReadOnly(),
            ]
        return super().get_permissions()


from rest_framework.views import APIView


class UserPublicProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    # get: Get a single public profile by user ID.
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['user_pk'])
        if user.is_instructor == False:
            user_public_profile_serializer = StudentPublicProfileSerializer(user.student_profile, many=False)
        if user.is_instructor == True:
            user_public_profile_serializer = InstructorPublicProfileSerializer(user.instructor_profile, many=False)
        return Response(user_public_profile_serializer.data, status=status.HTTP_200_OK)


class InstructorSkillCreateView(generics.CreateAPIView):
    serializer_class = InstructorSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomRenderer]
    queryset = InstructorSkill.objects.all()

    def perform_create(self, serializer):
        # Ensure user is an instructor in order to add a skill
        if not self.request.user.is_instructor:
            raise validator.ValidationError(
                                            {
                                            "detail": "User must have is_instructor = True to add a Skill"
                                            }
                                            )
        instructor_profile = get_object_or_404(InstructorProfile, user=self.request.user)
        serializer.save(instructor=instructor_profile)

class InstructorSkillListView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = InstructorSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomRenderer]
    pagination_class     = CustomPagination
    queryset = InstructorSkill.objects.all()
    

    def get_queryset(self):
        return super().get_queryset().filter(instructor__user__is_active=True)


class InstructorSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorSkillSerializer
    permission_classes = [custom_permissions.IsCreatorOrReadOnly]
    renderer_classes = [CustomRenderer]

    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(InstructorSkill, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
class SkillCertificationCreateView(generics.CreateAPIView):
    serializer_class = SkillCertificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomRenderer]
    queryset = SkillCertification.objects.all()
    
    def perform_create(self, serializer):
        skill_id = self.kwargs["pk"]
        instructor = get_object_or_404(InstructorProfile, user=self.request.user)
        instance = instructor.insructor_skill.filter(id=skill_id).first()
        
        if not self.request.user.is_instructor:
            raise validators.ValidationError(
                                            {
                                            "detail": "User must have is_instructor = True to create a certificate"        
                                            }
                                            )
        try:    
            serializer.save(skill=instance)
        except IntegrityError:
            raise validators.ValidationError(
                                            {
                                            "detail": "There is a certificate for this skill already!"
                                            }
                                            )
    
class SkillCertificationListView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = SkillCertificationSerializer
    pagination_class = CustomPagination
    renderer_classes = [CustomRenderer]
    queryset = SkillCertification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        instructor_id = self.request.query_params.get("instructor_id")
        
        if instructor_id:
            return super().get_queryset().filter(skill__instructor__user__is_active=True, \
                                                    skill__instructor__id=instructor_id)
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().none()
    
    
class SkillCertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillCertificationSerializer 
    permission_classes = [custom_permissions.IsCreatorOrReadOnly]
    renderer_classes = [CustomRenderer]
    
    def get_object(self):
        skill_id = self.kwargs["skill_pk"]
        cert_id = self.kwargs["cert_pk"]
        obj = get_object_or_404(SkillCertification, skill__id=skill_id, id=cert_id)
        self.check_object_permissions(self.request, obj)
        return obj 
    
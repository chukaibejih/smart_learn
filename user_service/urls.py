from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from user_service.views import UserViewSet, CustomTokenObtainPairViewSet, SMSCodeView, ConfirmEmailView,  StudentProfileViewset, InstructorProfileViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('student_profiles', StudentProfileViewset, basename="profiles")
router.register('instructor_profiles', InstructorProfileViewset, basename="profiles")

urlpatterns = router.urls + [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', CustomTokenObtainPairViewSet.as_view(), name='token-obtain-pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    path('confirm-email/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('smscode/', SMSCodeView.as_view(), name='sms_code'),

    path('user_public_profile/<str:user_pk>/', views.UserPublicProfileAPIView.as_view(), name='user_public_profile'),
    
    path("instructor/skills/", views.InstructorSkillListView.as_view(), name="instructor-skills"),
    path("instructor/skills/create-skill/", views.InstructorSkillCreateView.as_view(), name="create-skill"),
    path("instructor/skills/certificates/", views.SkillCertificationListView.as_view(), name="skill-certificates-list"),
    path("instructor/skills/<str:pk>/", views.InstructorSkillDetailView.as_view(), name="skill-details"),
    path("instructor/skills/<str:pk>/create-certificate/", views.SkillCertificationCreateView.as_view(), name="create-skill-certificate"),
    path("instructor/skills/<str:skill_pk>/certificates/<str:cert_pk>/", views.SkillCertificationDetailView.as_view(), name="skill-certificate-detail"),
]

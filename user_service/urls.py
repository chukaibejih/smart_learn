from django.urls import path, include
from rest_framework.routers import SimpleRouter
from user_service.views import UserViewSet, CustomTokenObtainPairViewSet, ConfirmEmailView,  StudentProfileViewset, InstructorProfileViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('student_profile', StudentProfileViewset, basename="profiles")
router.register('instructor_profile', InstructorProfileViewset, basename="profiles")

urlpatterns = router.urls + [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', CustomTokenObtainPairViewSet.as_view(), name='token-obtain-pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    path('confirm-email/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
]
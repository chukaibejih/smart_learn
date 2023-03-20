from django.urls import path
from rest_framework.routers import SimpleRouter
from user_service.views import UserViewSet, CustomTokenObtainPairViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls + [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', CustomTokenObtainPairViewSet.as_view(), name='token-obtain-pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
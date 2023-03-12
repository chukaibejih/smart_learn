from django.urls import path
from rest_framework.routers import SimpleRouter
from user_service.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls + [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
]
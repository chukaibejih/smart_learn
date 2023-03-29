from django.urls import path 
from course_service import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("course", views.CourseViewSet, basename="course")

urlpatterns = [
    
] + router.urls


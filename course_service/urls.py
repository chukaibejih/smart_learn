from django.urls import path, include
from course_service import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("course", views.CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
    path("course/<str:pk>/create-review/", views.ReviewCreateView.as_view(), name="create-review"),
    path("course/<str:pk>/reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("review/<str:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),
    path("instructor/skills/", views.InstructorSkillListView.as_view(), name="instructor-skills"),
    path("instructor/skills/create-skill/", views.InstructorSkillCreateView.as_view(), name="create-skill"),
    path("instructor/skills/<str:pk>/", views.InstructorSkillDetailView.as_view(), name="skill-details"),
]



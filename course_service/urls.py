from django.urls import path, include
from course_service import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.CourseViewSet, basename="course")
router.register('tag', views.TagView, basename='tags')
router.register('tag-module', views.TagModuleView, basename='tag-modules')


urlpatterns = [
    path("", include(router.urls)),
    path("course/<str:pk>/create-review/", views.ReviewCreateView.as_view(), name="create-review"),
    path("course/<str:pk>/reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("review/<str:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),
    path("instructor/skills/", views.InstructorSkillListView.as_view(), name="instructor-skills"),
    path("instructor/skills/create-skill/", views.InstructorSkillCreateView.as_view(), name="create-skill"),
    path("instructor/skills/certificates/", views.SkillCertificationListView.as_view(), name="skill-certificates-list"),
    path("instructor/skills/<str:pk>/", views.InstructorSkillDetailView.as_view(), name="skill-details"),
    path("instructor/skills/<str:pk>/create-certificate/", views.SkillCertificationCreateView.as_view(), name="create-skill-certificate"),
    path("instructor/skills/<str:skill_pk>/certificates/<str:cert_pk>/", views.SkillCertificationDetailView.as_view(), name="skill-certificate-detail"),
    path('<str:course_pk>/modules/', views.ModuleView.as_view({'get': 'list', 'post': 'create'}), name='module-list'),
    path('<str:course_pk>/modules/<str:pk>/', views.ModuleView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='module-detail'),
] 


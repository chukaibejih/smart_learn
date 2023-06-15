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

    path('<str:course_pk>/modules/', views.ModuleView.as_view({'get': 'list', 'post': 'create'}), name='module-list'),
    path('<str:course_pk>/modules/<str:pk>/', views.ModuleView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='module-detail'),

    path('<str:course_pk>/modules/<str:module_pk>/lesson/', views.LessonView.as_view({'get': 'list', 'post': 'create'}), name='lesson-list'),
    path('<str:course_pk>/modules/<str:module_pk>/lesson/<str:pk>/', views.LessonView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='lesson-detail'),
    path('<str:course_pk>/modules/<str:module_pk>/lesson/<str:lesson_pk>/quiz/', views.QuizView.as_view({'get': 'list', 'post': 'create'}), name='quiz-list'),
    path('<str:course_pk>/modules/<str:module_pk>/lesson/<str:lesson_pk>/quiz/<str:pk>/', views.QuizView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='quiz-detail'),
] 



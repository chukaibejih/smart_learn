from django.urls import path
from .views import EnrollmentByCourseView, EnrollmentView, StripeView

urlpatterns = [
    path('', EnrollmentView.as_view(), name='enrol'),
    path('pay/', StripeView.as_view(), name='pay'),
    path('<str:course_id>/', EnrollmentByCourseView.as_view(),
         name='enrollment-by-course')
]

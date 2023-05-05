from django.urls import path
from .views import EnrollmentView, StripeView

urlpatterns = [
    path('', EnrollmentView.as_view(), name='enroll'),
    path('pay/', StripeView.as_view(), name='pay')
]
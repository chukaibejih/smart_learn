from django.urls import path
from .views import EnrollmentView, StripeView

urlpatterns = [
    path('', EnrollmentView.as_view(), name='enrol'),
    path('pay/', StripeView.as_view(), name='pay')
]
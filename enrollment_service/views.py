from common.pagination import CustomPagination
from common.permissions import IsCourseInstructor
from rest_framework import (
    viewsets,
    permissions,
    generics,
    serializers,
    validators,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from course_service.models import Course
from .serializers import EnrollmentByCourseSerializer, EnrollmentSerializer, StripeSerializer
from .models import Enrollment

import stripe
from django.conf import settings
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EnrollmentFilter
# Create your views here.


class EnrollmentView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class EnrollmentByCourseView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = EnrollmentByCourseSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EnrollmentFilter
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Enrollment.objects.filter(course__id=course_id).order_by('-enrollment_date')


class PaymentView():
    pass


class StripeView(generics.CreateAPIView):
    serializer_class = StripeSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course = Course.objects.get(id=serializer.validated_data['course'])
            price = course.price
            user = request.user
            stripe.api_key = settings.STRIPE_SECRET
            intent = stripe.PaymentIntent.create(
                # Stripe uses cents instead of dollars
                amount=int(price * 100),
                currency="usd",
                description="Payment for " + course.name,
                receipt_email=user.email,
                automatic_payment_methods={"enabled": True},
            )
            response_data = {'client_secret': intent.client_secret}
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

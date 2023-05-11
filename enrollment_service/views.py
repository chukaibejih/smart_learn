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
from course_service.models import Course
from .serializers import EnrollmentSerializer, StripeSerializer
from .models import Enrollment

import stripe
from django.conf import settings

# Create your views here.


class EnrollmentView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


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
                amount=int(price * 100), # Stripe uses cents instead of dollars
                currency="usd",
                description = "Payment for " + course.name,
                receipt_email = user.email,
                automatic_payment_methods={"enabled": True},
            )
            response_data = {'client_secret': intent.client_secret}
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


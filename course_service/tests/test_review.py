from rest_framework.test import APITestCase 
from rest_framework import status
from course_service.models import Course, Review
from user_service.models import *
from django.urls import reverse 
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlencode
from password_generator import PasswordGenerator
# Create your tests here.


class ModelSetup:
    
    """
        Common setup cases for each test cases to avoid repitition of code.
    """
    
    def common_model_setup(self):
        pwg = PasswordGenerator()
        pwg.minlen = 10
        self.user1 = User.objects.create_user(
                                            first_name="John", 
                                            last_name="Doe" ,
                                            email="example1@gmail.com", 
                                            password=pwg.generate(), 
                                            is_instructor=True, 
                                            is_verified=True,
                                            enable_two_factor_authentication=False
                                            )
        self.user2 = User.objects.create_user(
                                            first_name="Michael", 
                                            last_name="Kruse" ,
                                            email="example2@gmail.com", 
                                            password=pwg.generate(), 
                                            is_instructor=True, 
                                            is_verified=True,
                                            enable_two_factor_authentication=False
                                            )
        instructors = InstructorProfile.objects.all()
        self.instructor1 = instructors[0]
        self.instructor2 = instructors[1]
        self.course1 = Course.objects.create(
                                            name="Fullstack Python/Django course for beginners - 2023",
                                            instructor=self.instructor1,
                                            difficulty="Intermediate",
                                            is_certified=True,
                                            is_available=True
                                           )
        self.course2 = Course.objects.create(
                                            name="Golang course for beginners - 2023",
                                            instructor=self.instructor2,
                                            difficulty="Intermediate",
                                            is_certified=False,
                                            is_available=True
                                           )
        
        refresh = RefreshToken.for_user(self.user1)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")



# Review Test Cases
class ReviewTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        super().common_model_setup()
        self.review = Review.objects.create(user=self.user1, course=self.course1,\
                                            comment="Nice course", rating=4.3)
    
    def test_create_review(self):
        from django.db import IntegrityError
        
        data = {
            "comment": "Nice Course",
            "rating": 4.0
        }
        url = reverse("create-review", args=[self.course2.id])
        response = self.client.post(url, data)
        course = Course.objects.get(id=self.course2.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(course.average_rating, 4.0)
        self.assertEqual(course.reviews, 1)
        
        # Create another review with the same user on the same course again
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["data"]["detail"], "This user has already created a review about this course")
        self.assertRaises(IntegrityError)
        
    def test_list_reviews(self):
        url = reverse("review-list", args=[self.course2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_review(self):
        data = {
            "comment": "Average Course",
            "rating": 3
        }
        url = reverse("review-detail", args=[self.review.pk])
        response = self.client.put(url, data)
        course = Course.objects.get(id=self.course1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(course.average_rating, 3.0)
        
    def test_delete_review(self):
        url = reverse("review-detail", args=[self.review.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        course = Course.objects.get(id=self.course1.id)
        self.assertEqual(course.average_rating, 0.0)
        self.assertEqual(course.reviews, 0)
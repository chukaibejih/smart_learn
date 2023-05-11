from rest_framework.test import APITestCase 
from rest_framework import status
from course_service.models import Course, Module, Lesson
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


class LessonTestCase(ModelSetup, APITestCase):
    # Inherited the ModelSetup class and called the setUp function
    def setUp(self) -> None:
        super().common_model_setup()
        self.module1 = Module.objects.create(
            name="Obejects",
            description="This module explains Objects",
            course=self.course1
        )
    
    def test_list_lesson(self):
        url = reverse("lesson-list", args=[self.course1.id, self.module1.id])
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
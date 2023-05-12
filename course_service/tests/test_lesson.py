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
        self.course3 = Course.objects.create(
                                            name="Django course for beginners - 2023",
                                            instructor=self.instructor1,
                                            difficulty="Intermediate",
                                            is_certified=True,
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
            name="Objects",
            description="This module explains Objects",
            course=self.course3
        )
    
    # Test that an authenticated user (including non-course instructors) can view a list of lessons for a particular module.
    def test_list_lesson(self):
        url = reverse("lesson-list", args=[self.course3.id, self.module1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.filter(module=self.module1).count(), 0)
    
    # Test that an authenticated course instructor can create a new lesson for their own course module.
    def test_create_lesson(self):
        url = reverse("lesson-list", args=[self.course3.id, self.module1.id])
        data = {
            "name": "How to create an object",
            "description": "This lesson will teach beginners how to create an object",
            "module": self.module1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(module=self.module1).count(), 1)
        self.assertEqual(response.data['name'], "How to create an object")

    # Test that an authenticated course instructor cannot create a new lesson for a module that belongs to a course they are not an instructor of.
    def test_create_lesson_with_wrong_instructor(self):

        refresh = RefreshToken.for_user(self.user2)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
    
        url = reverse("lesson-list", args=[self.course3.id, self.module1.id])
        data = {
            "name": "How to create an object",
            "description": "This lesson will teach beginners how to create an object",
            "module": self.module1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "You cannot create a new lesson for a module that belongs to a course you are not an instructor of.")

    # Test that an unauthenticated user cannot create a new lesson.
    def test_create_lesson_with_wrong_instructor(self):

        self.client.credentials(HTTP_AUTHORIZATION= "")
    
        url = reverse("lesson-list", args=[self.course3.id, self.module1.id])
        data = {
            "name": "How to create an object",
            "description": "This lesson will teach beginners how to create an object",
            "module": self.module1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    # Test that a student or non-instructor staff user cannot create a new lesson.
    def test_create_lesson_with_is_instructor_false(self):

        self.user2.is_instructor = False
        self.user2.save()
        refresh = RefreshToken.for_user(self.user2)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
    
        url = reverse("lesson-list", args=[self.course3.id, self.module1.id])
        data = {
            "name": "How to create an object",
            "description": "This lesson will teach beginners how to create an object",
            "module": self.module1.id
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "User must have is_instructor = True to create a course")

    # Test that an authenticated course instructor can update their lesson. 
    def test_update_lesson(self):
        self.lesson1 = Lesson.objects.create(
            name="How to create an object",
            description="This lesson will teach beginners how to create an object",
            module=self.module1
        )

        url = reverse("lesson-detail", args=[self.course3.id, self.module1.id, self.lesson1.id])
        data = {
            "description": "This lesson will teach beginners how to create an object in Django",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "This lesson will teach beginners how to create an object in Django")

    # Test that an authenticated course instructor can delete their lesson. 
    def test_delete_lesson(self):
        self.lesson1 = Lesson.objects.create(
            name="How to create an object",
            description="This lesson will teach beginners how to create an object",
            module=self.module1
        )
        url = reverse("lesson-detail", args=[self.course3.id, self.module1.id, self.lesson1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)



        

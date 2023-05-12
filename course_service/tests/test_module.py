from rest_framework.test import APITestCase 
from rest_framework import status
from course_service.models import Course, Module
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



# Test cases for modules       
class ModuleTestCase(ModelSetup, APITestCase):

    # Inherited the ModelSetup class and called the setUp function
    def setUp(self) -> None:
        return super().common_model_setup()

    # Test case to list the modules for a particular course
    def test_list_modules(self):
        url = reverse("module-list", args=[self.course1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(Module.objects.filter(course=self.course1).count())
        self.assertEqual(Module.objects.filter(course=self.course1).count(), 0)

        # Add a module to the course and check if it's returned
        data = {
            "name": "Introduction",
            "description": "This module gives an introduction to the course",
            "course": self.course1.id
        }
        self.client.post(url, data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Introduction")

    # Test case to retrieve a module details by passing in the module id and the course id 
    def test_retrieve_module(self):
        module = Module.objects.create(
            name="Loops",
            description="This module explains loops",
            course=self.course2
        )
        url = reverse("module-detail", args=[self.course2.id, module.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Loops")

    # Test case to create a module for a course
    def test_create_module(self):
        data = {
            "name": "Loops",
            "description": "This module explains loops",
            "course": self.course1.id
        }
        url = reverse("module-list", args=[self.course1.id])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.first().name, "Loops")

    # Test case to create a module for a course belonging to another instructor
    def test_create_module_for_other_instructor_course(self):
        data = {
            "name": "Introduction",
            "description": "This module gives an introduction to the course",
            "course": self.course2.id
        }
        url = reverse("module-list", args=[self.course2.id])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Module.objects.count(), 0)

    # Test case for updating a module
    def test_update_module(self):
        module = Module.objects.create(
            name="Loops",
            description="This module explains loops",
            course=self.course1
        )
        data = {
            "name": "Loops in Python",
            "description": "This module explains loops in Python",
            "course": self.course1.id
        }
        url = reverse("module-detail", args=[self.course1.id, module.id])
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.first().name, "Loops in Python")

    # Test case to delete a module belonging to a particular course
    def test_delete_module(self):
        module = Module.objects.create(
            name="Loops",
            description="This module explains loops",
            course=self.course1
        )
        url = reverse("module-detail", args=[self.course1.id, module.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.count(), 0)
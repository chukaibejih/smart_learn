from rest_framework.test import APITestCase 
from rest_framework import status
from .models import *
from user_service.models import *
from django.urls import reverse 
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlencode
from password_generator import PasswordGenerator
# Create your tests here.


class ModelSetup:
    
    
    def common_model_setup(self):
        pwg = PasswordGenerator()
        pwg.minlen = 10
        self.user1 = User.objects.create_user(
                                            first_name="John", 
                                            last_name="Doe" ,
                                            email="example1@gmail.com", 
                                            password=pwg.generate(), 
                                            is_instructor=True, 
                                            is_verified=True
                                            )
        self.user2 = User.objects.create_user(
                                            first_name="Michael", 
                                            last_name="Kruse" ,
                                            email="example2@gmail.com", 
                                            password=pwg.generate(), 
                                            is_instructor=True, 
                                            is_verified=True
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
        

class CourseTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        return super().common_model_setup()
    
    def test_create_course(self):
        data = {
            "name": "Full Stack MERN course for beginners - 2023",
            "difficulty": "Advanced",
            "is_certified": True,
            "is_available": True,
            "description": "None",
            "duration": "23hrs 40mins"
        }
        url = reverse("course-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["data"]["instructor"], self.instructor1.id)
        self.assertEqual(Course.objects.count(), 3)
        
    def test_create_course_with_is_instructor_false(self):
        self.user2.is_instructor = False 
        self.user2.save()
        refresh = RefreshToken.for_user(self.user2)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
        data = {
            "name": "Full Stack MERN course for beginners - 2023",
            "difficulty": "Beginner",
            "is_certified": True,
            "is_available": True,
            "description": "None",
            "duration": "23hrs 40mins"
        }
        url = reverse("course-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["data"]["detail"], "User must have is_instructor = True to create a course")
        
    def test_list_courses(self):
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_courses_filter(self):
        url = f"{reverse('course-list')}?{urlencode({'is_certified': 'False'})}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["results"][0]["name"], "Golang course for beginners - 2023")
        
    def test_retrieve_course(self):
        url = reverse("course-detail", args=[self.course1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_course(self):
        data = {
            "is_available": False
        }
        url = reverse("course-detail", args=[self.course1.id])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["is_available"], False)
        
    def test_update_course(self):
        data = {
            "is_available": False,
            "description": f"Django Course by {self.course1.get_instructor_fullname}",
        }
        url = reverse("course-detail", args=[self.course1.id])
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["description"], "Django Course by John Doe")
        
    
        
class ReviewTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        return super().common_model_setup()
    
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
        
    
        
        

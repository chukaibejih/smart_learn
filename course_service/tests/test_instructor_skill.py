from rest_framework.test import APITestCase 
from rest_framework import status
from course_service.models import Course, InstructorSkill
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


class InstructorSkillTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        super().common_model_setup()
        self.skill1 = InstructorSkill.objects.create(
                                                     instructor=self.instructor1,
                                                     skill_name="DevOps Engineering",
                                                     skill_level=5   
                                                    )
        self.skill2 = InstructorSkill.objects.create(
                                                     instructor=self.instructor1,
                                                     skill_name="Backend Development",
                                                     skill_level=5   
                                                    )
    
    def test_create_skill(self):
        data = {
            "skil_name": "Frontend Development",
            "skill_level": 4
        }
        url = reverse("create-skill")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_skill_by_non_instructor(self):
        self.user1.is_instructor = False
        self.user1.save()
        
        data = {
            "skil_name": "Frontend Development",
            "skill_level": 4
        }
        url = reverse("create-skill")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_list_skill_data(self):
        url = reverse("instructor-skills")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]["results"]), InstructorSkill.objects.count())
        
        
    def test_retrieve_skill_data(self):
        url = reverse("skill-details", args=[self.skill1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_partial_update_skill_data(self):
        data = {
            "skill_level": 4
        }
        url = reverse("skill-details", args=[self.skill1.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_skill_data(self):
        url = reverse("skill-details", args=[self.skill1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
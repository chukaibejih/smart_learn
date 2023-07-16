from django.test import TestCase
from enrollment_service.serializers import EnrollmentByCourseSerializer
from password_generator import PasswordGenerator
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from user_service.models import StudentProfile, User, InstructorProfile
from course_service.models import Course
from .models import Enrollment
from django.urls import reverse


class EnrollmentByCourseViewTestCase(TestCase):
    def setUp(self):
        # Creating Users
        pwg = PasswordGenerator()
        pwg.minlen = 10
        self.client = APIClient()
        self.stu1 = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="example1@gmail.com",
            password=pwg.generate(),
            is_instructor=False,
            is_verified=True,
            enable_two_factor_authentication=False
        )

        self.stu2 = User.objects.create_user(
            first_name="Michael",
            last_name="Kruse",
            email="example2@gmail.com",
            password=pwg.generate(),
            is_instructor=False,
            is_verified=True,
            enable_two_factor_authentication=False
        )

        students = StudentProfile.objects.all()

        self.ins1 = User.objects.create_user(
            first_name="Naruto",
            last_name="Uzumaki",
            email="example3@gmail.com",
            password=pwg.generate(),
            is_instructor=True,
            is_verified=True,
            enable_two_factor_authentication=False
        )
        self.ins2 = User.objects.create_user(
            first_name="Sasuke",
            last_name="Uchiha",
            email="example4@gmail.com",
            password=pwg.generate(),
            is_instructor=True,
            is_verified=True,
            enable_two_factor_authentication=False
        )
        instructors = InstructorProfile.objects.all()

        self.course1 = Course.objects.create(
            name="Fullstack Python/Django course for beginners - 2023",
            instructor=instructors[0],
            difficulty="Intermediate",
            is_certified=True,
            is_available=True
        )
        self.course2 = Course.objects.create(
            name="Golang course for beginners - 2023",
            instructor=instructors[1],
            difficulty="Intermediate",
            is_certified=False,
            is_available=True
        )

        # Enrolling students to courses
        # Course 1
        self.enrollment1 = Enrollment.objects.create(
            student=students[0], course=self.course1)
        self.enrollment2 = Enrollment.objects.create(
            student=students[1], course=self.course1)

        # Course 2
        self.enrollment3 = Enrollment.objects.create(
            student=students[1], course=self.course2)

        # Authentication
        refresh = RefreshToken.for_user(instructors[0])
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Enrollment url
        self.course1_enrollment_url = reverse(
            'enrollment-by-course', args=[self.course1.id])
        self.course2_enrollment_url = reverse(
            'enrollment-by-course', args=[self.course2.id])
        self.dummy_course = reverse('enrollment-by-course', args=['random'])

    # Test to find whether the response contains correct status code

    def test_enrollment_by_course_200_status_code(self):
        response = self.client.get(self.course1_enrollment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Whether the response is correct for course1

    def test_enrollment_by_course_response_for_course1(self):
        response = self.client.get(self.course1_enrollment_url)

        enrollments = Enrollment.objects.filter(
            course=self.course1).order_by('-enrollment_date')
        expected_data = EnrollmentByCourseSerializer(
            enrollments, many=True).data
        self.assertEqual(response.data['results'], expected_data)

    # Whether the response is correct for course2

    def test_enrollment_by_course_response_for_course2(self):
        response = self.client.get(self.course2_enrollment_url)

        enrollments = Enrollment.objects.filter(
            course=self.course2).order_by('-enrollment_date')
        expected_data = EnrollmentByCourseSerializer(
            enrollments, many=True).data
        self.assertEqual(response.data['results'], expected_data)

    # If course not found

    def test_enrollment_by_course_response_for_invalid_or_none_enrolled_course(self):
        response = self.client.get(self.dummy_course)

        enrollments = Enrollment.objects.filter(
            course='random').order_by('-enrollment_date')
        expected_data = EnrollmentByCourseSerializer(
            enrollments, many=True).data
        self.assertEqual(response.data['results'], expected_data)

    # Date range filter test

    def test_enrollment_by_course_date_range_filter(self):
        response = self.client.get(
            self.course1_enrollment_url + '?enrollment_date_after=2023-07-15')

        enrollments = Enrollment.objects.filter(
            course=self.course1).order_by('-enrollment_date').filter(enrollment_date__gte='2023-07-15')
        expected_data = EnrollmentByCourseSerializer(
            enrollments, many=True).data

        self.assertEqual(response.data['results'], expected_data)

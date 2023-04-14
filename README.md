# Smart Learning(Work In Progress)

This is an API for a Smart Learning project built with Django Rest Framework (DRF). The API allows users to enroll in courses, complete lessons and quizzes, and track their progress. Instructors can create and manage courses, lessons, and quizzes, as well as view information about enrolled users.

System Architecture
---------------

![Smart Leraning Microservices (2)](https://user-images.githubusercontent.com/29266211/223722821-d64cbe95-6a67-4f99-bf72-0bfffe675378.jpg)


ER Diagram
---------------
![Smart Learn (2)](https://user-images.githubusercontent.com/29266211/229353168-cc3c2af8-61cc-4d8f-a9f5-02b8ad2c1357.png)

link: https://dbdiagram.io/d/64087c2f296d97641d865ec8

Getting Started
---------------

To run the API locally, follow these steps:

1.  Clone the repository: `git clone https://github.com/yourusername/smart-learning-api.git`
2.  Create a virtual environment: `python -m venv env`
3.  Activate the virtual environment: `source env/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Set up the database: `python manage.py migrate`
6.  Create a superuser account: `python manage.py createsuperuser`
7.  Start the development server: `python manage.py runserver`

Authentication
--------------

Authentication is required for most endpoints in the API. To authenticate, include an access token in the `Authorization` header of your request. The access token can be obtained by logging in to your account or registering a new account.

API Endpoints
-------------

The following endpoints are available in the API:

### Authentication Endpoints

-   `/api/auth/register/` (POST): to allow users to register for an account.
-   `/api/auth/login/` (POST): to allow users to log in to their account.
-   `/api/auth/logout/` (POST): to allow users to log out of their account.

### User Profile Endpoints

-   `/api/users/` (GET): to retrieve a list of all registered users.
-   `/api/users/<user_id>/` (GET, PUT, PATCH, DELETE): to retrieve, update, partially update or delete a specific user's profile.

### Course Endpoints

-   `/api/courses/` (GET): to retrieve a list of all available courses.
-   `/api/courses/<course_id>/` (GET): to retrieve information about a specific course.
-   `/api/courses/<course_id>/enroll/` (POST): to allow a user to enroll in a specific course.

### Lesson Endpoints

-   `/api/courses/<course_id>/lessons/` (GET): to retrieve a list of all lessons in a specific course.
-   `/api/courses/<course_id>/lessons/<lesson_id>/` (GET): to retrieve information about a specific lesson.
-   `/api/courses/<course_id>/lessons/<lesson_id>/progress/` (POST): to update a user's progress in a specific lesson.

### Quiz Endpoints

-   `/api/courses/<course_id>/lessons/<lesson_id>/quizzes/` (GET): to retrieve a list of all quizzes in a specific lesson.
-   `/api/courses/<course_id>/lessons/<lesson_id>/quizzes/<quiz_id>/` (GET): to retrieve information about a specific quiz.
-   `/api/courses/<course_id>/lessons/<lesson_id>/quizzes/<quiz_id>/submit/` (POST): to allow a user to submit answers for a specific quiz.

### Instructor Endpoints

-   `/api/instructors/` (GET): to retrieve a list of all registered instructors.
-   `/api/instructors/<instructor_id>/` (GET, PUT, PATCH, DELETE): to retrieve, update, partially update or delete a specific instructor's profile.
-   `/api/courses/` (POST): to allow an instructor to create a new course.
-   `/api/courses/<course_id>/` (PUT, PATCH, DELETE): to allow an instructor to update or delete a specific course.
-   `/api/courses/<course_id>/lessons/` (POST): to allow an instructor to create a new lesson within a specific course.
-   `/api/courses/<course_id>/lessons/<lesson_id>/` (PUT, PATCH, DELETE): to allow an instructor to update or delete a specific lesson within a course.
-   `/api/courses/<course_id>/lessons/<lesson_id>/quizzes/` (POST): to allow an instructor to create a new quiz within a specific lesson.
-   `/api/courses/<course_id>/lessons/<lesson_id>/quizzes/<quiz_id>/` (PUT, PATCH, DELETE): to allow an instructor to update or delete a specific quiz within a lesson.
-   `/api/courses/<course_id>/enrollments/` (GET): to retrieve a list of all users

Contributing
------------

Contributions to this project are welcome! To get started, fork the repository and create a new branch for your feature or bug fix. Once you've made your changes, submit a pull request for review.


License
-------

This project is licensed under the MIT License - see the [LICENSE.md](https://chat.openai.com/chat/LICENSE.md) file for details.

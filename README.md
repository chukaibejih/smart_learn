# Smart Learning(Work In Progress)

This Smart Learning API is built with Django Rest Framework (DRF) and provides a powerful set of features for both users and instructors. With this API, users can enroll in courses, and complete modules, lessons and quizzes. Instructors can create and manage courses, modules, lessons, and quizzes, as well as view information about enrolled users.

This Smart Learning API is designed to be flexible and easy to use. Using Swagger/OpenAPI to provide you with a clean and intuitive API interface that makes it easy for developers to integrate with other systems. Whether you're building a mobile app, a web-based learning platform, or something else entirely.

System Architecture
---------------

![service diagram drawio (2)](https://github.com/chukaibejih/smart_learn/assets/29266211/ca34cf71-0a69-44ff-9555-2f4f2ea65ac0)



ER Diagram
---------------
![Smart Learn (2)](https://user-images.githubusercontent.com/29266211/229353168-cc3c2af8-61cc-4d8f-a9f5-02b8ad2c1357.png)

link: https://dbdiagram.io/d/64087c2f296d97641d865ec8

Getting Started
---------------

To run the API locally, follow these steps:

1.  Clone the repository: `git clone https://github.com/yourusername/smart-learning-api.git`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Go to .settings.DATABASES section, deactivate #PRODUCTION mode and activate #Development mode, add PostgreSQL configuration to connect to your database to be the default database.
6.  Change `.env.templates` to .env and setup your environment variables. 
7.  Set up the database: `python manage.py migrate`
8.  Create a superuser account: `python manage.py createsuperuser`
9.  Start the development server: `python manage.py runserver`

To run the API locally, with Docker and Docker Compose, follow these steps:

1. Go to .settings.DATABASES section, deactivate #PRODUCTION mode and activate #Development mode, add PostgreSQL configuration to connect to your database to be the default database.
2. Change `.env.templates` to .env and setup your environment variables.
3. Start application and database integration: `sudo docker compose -f docker-compose.yaml up --build`
4. Stop and clear integration: `sudo docker compose -f docker-compose.yaml down`

Running Tests
---------------

Tests are organized into different files within the app's `tests` directory. Here's how to run them:

1. To run all the tests, use the following command:

    ```
    python manage.py test
    ```

2. To run a single test file, you can use the following command (replacing `<app_name>` and `<test_file>` with the appropriate values):

    ```
    python manage.py test <app_name>.tests.<test_file>
    ```


Functional Requirements Definition
--------------

Functional requirements specify the actions that a software system or application should take to satisfy the user's needs and business objectives. They describe the system's functions, features, and capabilities, as well as how it should respond under different circumstances.

- User Authentication: The API should provide a user registraion, log-in and email confimation functionality, including password recovery features. We’ll ensure that passwords are securely stored and hashed using Django’s built-in authentication system.

- Profile Management: Users should be able to manage and update their profile information, including profile pictures.

- Course Enrollment: The API should allow users to enroll in courses. 

- Instructor Course Creation: Instructors should be able to create new courses, add modules, lessons, and quizzes to them using the API.

- Instructor Course Management: Instructors should be able to manage their courses, including editing or deleting course content, modules, lessons, and quizzes using the API.

- Payment: Users should be able to make course payments through the API after enrolling.


Tech Stack
--------------

- Language: Python 3.10
- Framework: Django 4.0+
- Database: PostgreSQL
- API USED: Strip - Test mode
- Testing: Django Test Framework
- Test Coverage: 80%+
- Development Methodology: TDD (Test Driven Development)


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
-   `/api/auth/smscode/` (POST): to allow users verfiy SMS verfication code

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


Limitations
------------

While the Smart Learning API is designed to be a flexible and powerful tool for users and instructors alike, there are some limitations to consider when using this system:

- Lack of support for multimedia content: At the moment, the API does not support multimedia content such as videos, images or audio files. This can limit the types of courses that can be offered through the platform.
- Limited payment options: Currently, the only payment option available for users is through the Stripe API. This may not be ideal for some users who prefer to use other payment methods.
- No support for multiple languages: The API currently only supports content in English. This may be a limitation for users who prefer to learn in other languages.
- Limited reporting and analytics: While the API provides some basic reporting and analytics features, these may not be sufficient for more advanced reporting needs.
- Limited customization options: The API provides a basic set of features and customization options, but may not be ideal for users who require a highly customized learning platform.


Contributing
------------

Contributions to this project are welcome! Go through our [GUIDELINES](https://github.com/chukaibejih/smart_learn/blob/main/CONTRIBUTING.md)


License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

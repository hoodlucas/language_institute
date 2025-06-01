Capstone Project: Course Management System

Overview

This project is a Course Management System designed for teachers to organize and manage their courses, students, class sessions, attendance, grades, and uploaded materials. The platform is built using Django on the backend and includes JavaScript-based interactivity for an enhanced user experience. The system is fully mobile-responsive, structured, and user-friendly, allowing teachers to efficiently manage multiple academic tasks from a centralized dashboard.


Distinctiveness

Unlike the e-commerce or social network examples in CS50W, this system is tailored specifically for academic use and designed to simplify educational administrative workflows. The system includes modules such as:

Multi-schedule course creation and editing

Class session planning with material uploads

Student management (with course associations)

Attendance tracking with justifications

Grade assignment and observation logging

This structure provides a distinct functionality set not found in any of the other course projects.


Complexity

The system integrates multiple relational models such as Course, Schedule, ClassSession, Student, Attendance, Grade, and Observation, each with logical connections and access control based on the currently logged-in teacher. JavaScript is used dynamically to manage inputs like adding schedules on the fly. The views.py file contains over 40 custom views with logic covering authentication, CRUD operations, and student statistics (like attendance percentages). It is far more advanced than the early projects and reflects a full-stack implementation.


Features

User Registration/Login/Logout for teachers

Course Creation & Editing, supporting multiple schedules (day, time range)

Class Session Management, including topic, note, and date

File Uploads for materials per class session

Attendance Tracking, with present/absent/justified states

Student Management: Add/edit/delete and assign to multiple courses

Grades & Observations, attached to students per course

Statistical Dashboard for attendance per student with percentage

Clean and responsive design with Bootstrap 5


File Structure Summary

views.py: All backend logic and request handling

models.py: All data models (Course, Student, Session, Attendance, etc.)

templates/dashboard/: All HTML templates for each view (dashboard, forms, detail views)

static/: Custom styles and JavaScript

urls.py: URL routing for all views

requirements.txt: Python package dependencies

README.md: Project documentation (this file)


JavaScript Integration

Used to:

Dynamically add schedules when creating/editing a course

Remove schedule fields instantly

Improve UX with Bootstrap components


Mobile Responsiveness

All pages use Bootstrap 5 grid layout to ensure full compatibility with mobile devices. Components such as buttons, cards, and forms scale appropriately on small screens.


How to Run the Application

Clone the repository:

git clone https://github.com/yourusername/course-management-system.git
cd course-management-system

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Run the development server:

python manage.py runserver

Access the app at http://127.0.0.1:8000


Requirements

Django==5.2
sqlparse==0.5.3
asgiref==3.8.1
tzdata==2025.2


Additional Notes

The app uses Django's default User model to manage authentication.

Each Teacher is tied to a user, and all resources are filtered accordingly.

Includes error handling for duplicate users, missing fields, and unauthorized access.

Minimal external packages are used for better maintainability.
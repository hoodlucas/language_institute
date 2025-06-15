
# Course Management System

## Overview

The Course Management System is a web-based application that allows teachers to fully organize and administrate their courses, students, class sessions, assignments, grades, and attendance records. Designed with educational institutions in mind, the system centralizes multiple administrative tasks into a single intuitive interface, facilitating class preparation, tracking student progress, and managing course materials.

The system is built using Django as backend framework and JavaScript to handle client-side interactivity. Its architecture allows teachers to manage schedules, upload materials, track attendance with justification features, assign grades, and monitor academic performance through a dynamic and responsive web interface.

## Distinctiveness and Complexity

This Course Management System addresses an educational administrative use case not covered in any of CS50W’s previous projects, such as e-commerce, email or social networking. The system was specifically designed for teachers to fully handle all aspects of academic course management, including courses, schedules, students, class sessions, materials, attendance, grades, and qualitative observations. No other project in CS50W approaches this level of administrative depth, making this application distinctly different.

### Distinctiveness

Unlike prior projects, this system introduces several highly specialized modules that make it stand apart:

- Multi-schedule Course Management: Each course supports multiple schedules (day + time ranges) allowing teachers to define complex recurring sessions across the week. Schedule entries are dynamically handled both server-side and via JavaScript frontend logic.
- Class Sessions & Materials: Teachers can create class sessions (tied to specific dates), assign topics, notes, and upload session-specific teaching materials (with file type validation and storage handling).
- Student Management: Students can be added, edited, assigned to one or multiple courses, and managed independently of class sessions.
- Attendance Tracking with Justifications: For every class session, attendance is recorded per student, with support for distinguishing between simple absences and justified absences.
- Grading System: Teachers can assign numeric grades to students, tied to both course and student instances.
- Observations Module: Teachers can add qualitative feedback (observations) for each student, independent of grades.
- Dashboard Statistics: The system computes and displays student attendance statistics, calculating presence percentages dynamically.

### Complexity

Beyond the distinct functionality, the technical implementation required advanced backend and frontend logic:

- 11 relational models: Teacher, Course, Schedule, ClassSession, Student, Attendance, Grade, Observation, Material, Assignment, AssignmentSubmission.
- Relationships include: One-to-One (User–Teacher), Many-to-Many (Student–Courses), and multiple ForeignKeys linking class sessions, materials, and attendance records.
- Uniqueness constraints are applied to ensure data consistency for sessions, submissions, and attendance records.
- Backend logic resides within a single views.py module containing over 40 distinct views covering CRUD operations, dynamic filtering, role-based access control, student-course assignments, attendance processing, and statistical calculations.
- All views enforce authentication and authorization, restricting data access to each teacher's own records.
- Teacher–User binding ensures isolation of data between users.
- JavaScript is used for dynamic schedule creation on course forms, adding and removing schedule fields instantly before form submission.
- File uploads with server-side file type validation and secure storage.
- Bootstrap 5 ensures mobile-friendly, responsive design across devices.
- Comprehensive error handling for duplicate users, student-course validations, unauthorized access, and secure file deletion.
- Attendance percentages are dynamically computed for each student using Django ORM aggregation.

This project integrates complex data modeling, role-based access control, asynchronous frontend interaction, server-side data consistency enforcement, and responsive interface design, exceeding the technical depth of prior CS50W assignments.

## Features

- User authentication (registration, login, logout)
- Teacher profile creation upon registration
- Course creation with multi-schedule support
- Class session creation, editing, and deletion
- File uploads for class materials with validation
- Student management across multiple courses
- Attendance tracking with present, absent, and justified states
- Automatic attendance statistics per student
- Grading system with descriptions and timestamps
- Observation module for qualitative feedback
- Secure file deletion
- Role-based access control limiting data to each teacher
- JavaScript-powered dynamic forms for schedules
- Error handling and validation throughout

## Models and Database Design

The system uses Django ORM with the following models:

- **User (Django built-in):** Authentication and basic user data.
- **Teacher:** One-to-One link to User, with phone and specialty fields.
- **Course:** Name, description, and assigned Teacher.
- **Schedule:** Linked to Course, defines class days and times.
- **ClassSession:** Linked to Course, with date, topic, and notes.
- **Student:** Student info, linked to multiple Courses.
- **Attendance:** Linked to ClassSession and Student, tracks presence and justification.
- **Assignment & AssignmentSubmission:** Handles homework with deadlines and submissions.
- **Grade:** Numeric grades per student per course.
- **Observation:** Qualitative notes from Teacher per student.
- **Material:** Uploaded files per ClassSession.

## File Structure

- `manage.py`: Django management script.
- `requirements.txt`: Dependencies list.
- `README.md`: Project documentation.
- `db.sqlite3`: Development database.
- `media/`: Uploaded materials.

### Project Modules

- `language_institute/`: Django project configuration.
- `dashboard/`: Main app (models, views, urls, admin, migrations).

### Templates

- `layout.html`: Base layout.
- `teacher_dashboard.html`: Main dashboard.
- `auth/`: Login and register pages.
- `student/`: Student management templates.
- `dashboard/`: Course/session management templates.

## URL Routes

### Authentication

- `/register/`, `/login/`, `/logout/`

### Courses & Dashboard

- `/`, `/course/create/`, `/course/edit/<course_id>/`, `/course/delete/<course_id>/`, `/course/<course_id>/`

### Class Sessions

- `/session/create/`, `/session/edit/<session_id>/`, `/session/delete/<session_id>/`

### Materials

- `/session/<session_id>/materials/upload/`, `/material/delete/<material_id>/`

### Students

- `/students/`, `/students/manage/`, `/student/add/`, `/student/edit/<student_id>/`, `/student/delete/<student_id>/`, `/student/remove/<course_id>/<student_id>/`

### Attendance

- `/attendance/<session_id>/`

### Observations & Grades

- `/student/<student_id>/add-observation/`, `/student/<student_id>/<course_id>/add-grade/`

## Views Overview

Backend logic in `dashboard/views.py` includes:

- Authentication (`register_teacher`, `login_teacher`, `logout_teacher`)
- Courses (`create_course`, `edit_course`, `delete_course`, `course_detail`)
- Class sessions (`create_class_session`, `edit_class_session`, `delete_class_session`)
- Materials (`upload_material`, `delete_material`)
- Students (`add_student`, `edit_student`, `delete_student`, etc.)
- Attendance (`take_attendance`)
- Observations & Grades (`add_observation`, `add_grade`)

## JavaScript Functionality

JavaScript enhances course creation/editing:

- Dynamic schedule field management.
- Form validation before submission.
- Integrated with Bootstrap 5 for UI consistency.

## CSS and Responsiveness

Bootstrap 5 ensures responsiveness across all devices. Minor custom CSS handles layout fine-tuning.

## How to Run the Application

1. Clone the repository:

```bash
git clone https://github.com/hoodlucas/language_institute.git
cd course-management-system
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Run the server:

```bash
python manage.py runserver
```

6. Access at `http://127.0.0.1:8000/`

## Requirements

```bash
Django==5.2
sqlparse==0.5.3
asgiref==3.8.1
tzdata==2025.2
```

## Additional Notes

- Django’s User model handles authentication.
- Per-teacher data isolation enforced on all views.
- File uploads are validated and securely stored.
- Attendance uniqueness enforced via database constraints.
- Multiple course enrollment per student supported.
- Robust error handling throughout.

## Acknowledgments

This project was developed as part of CS50’s Web Programming with Python and JavaScript, offered by Harvard University.

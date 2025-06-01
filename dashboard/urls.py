from django.urls import path
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", lambda request: redirect("login_teacher")),
    path("register/", views.register_teacher, name="register_teacher"),
    path("login/", views.login_teacher, name="login_teacher"),
    path("logout/", views.logout_teacher, name="logout_teacher"),
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("create-session/", views.create_class_session, name="create_class_session"),
    
    path("create-course/", views.create_course, name="create_course"),
    path("create-session/", views.create_class_session, name="create_class_session"),
    path("delete-course/<int:course_id>/", views.delete_course, name="delete_course"),
    path("edit-course/<int:course_id>/", views.edit_course, name="edit_course"),
    path("create-session/", views.create_class_session, name="create_class_session"),
    path("session/<int:session_id>/edit/", views.edit_class_session, name="edit_class_session"),
    path("session/<int:session_id>/delete/", views.delete_class_session, name="delete_class_session"),
    path("session/<int:session_id>/upload/", views.upload_material, name="upload_material"),
    path("material/<int:material_id>/delete/", views.delete_material, name="delete_material"),
    path("course/<int:course_id>/detail/", views.course_detail, name="course_detail"),
    
    path("students/", views.students_list, name="students_list"),
    path("students/", views.all_students, name="all_students"),
    path("course/<int:course_id>/add-student/", views.add_student_to_course, name="add_student_to_course"),
    path("students/add/", views.add_student, name="add_student"),
    path("student/<int:student_id>/edit/", views.edit_student, name="edit_student"),
    path("student/<int:student_id>/delete/", views.delete_student, name="delete_student"),
    path('course/<int:course_id>/remove_student/<int:student_id>/', views.remove_student_from_course, name='remove_student_from_course'),
    path('session/<int:session_id>/attendance/', views.take_attendance, name='take_attendance'),
    path('student/<int:student_id>/add_observation/', views.add_observation, name='add_observation'),
    path('student/<int:student_id>/course/<int:course_id>/add_grade/', views.add_grade, name='add_grade'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

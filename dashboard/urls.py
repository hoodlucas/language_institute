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
    path("course/<int:course_id>/sessions/", views.course_sessions, name="course_sessions"),
    path("session/<int:session_id>/edit/", views.edit_class_session, name="edit_class_session"),
    path("session/<int:session_id>/delete/", views.delete_class_session, name="delete_class_session"),
    path("session/<int:session_id>/upload/", views.upload_material, name="upload_material"),
    path("material/<int:material_id>/delete/", views.delete_material, name="delete_material"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

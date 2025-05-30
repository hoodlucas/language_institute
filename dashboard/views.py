from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Teacher, ClassSession, Course, Schedule, Material
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.utils.timezone import now
import os

# Create your views here.

def register_teacher(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        # Validación
        if password != confirmation:
            return render(request, "dashboard/register.html", {
                "message": "Passwords must match."
            })

        # Crear usuario
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except:
            return render(request, "dashboard/register.html", {
                "message": "Username already taken."
            })

        # Crear Teacher asociado
        Teacher.objects.create(user=user)

        # Login automático
        login(request, user)
        return redirect("teacher_dashboard")

    return render(request, "dashboard/register.html")



def login_teacher(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("teacher_dashboard")
        else:
            return render(request, "dashboard/login.html", {
                "message": "Invalid username or password."
            })

    return render(request, "dashboard/login.html")


def logout_teacher(request):
    logout(request)
    return redirect("login_teacher")



@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher).prefetch_related("schedules")
    
    return render(request, "dashboard/teacher_dashboard.html", {
        "teacher": teacher,
        "courses": courses
    })


@login_required
def create_course(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        days = request.POST.getlist("day")
        start_times = request.POST.getlist("start_time")
        end_times = request.POST.getlist("end_time")

        if name and days:
            course = Course.objects.create(
                name=name,
                description=description,
                teacher=teacher
            )

            for i in range(len(days)):
                day = days[i]
                start = start_times[i]
                end = end_times[i]
                if day and start and end:
                    Schedule.objects.create(
                        course=course,
                        day=day,
                        start_time=start,
                        end_time=end
                    )

            return redirect("teacher_dashboard")

    return render(request, "dashboard/create_course.html")


@login_required
def delete_course(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == "POST":
        course.delete()
        return redirect("teacher_dashboard")

    return render(request, "dashboard/delete_course.html", {"course": course})


@login_required
def edit_course(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)
    schedules = Schedule.objects.filter(course=course)

    if request.method == "POST":
        course.name = request.POST.get("name")
        course.description = request.POST.get("description")
        course.save()

        # eliminar horarios anteriores
        schedules.delete()

        days = request.POST.getlist("day")
        start_times = request.POST.getlist("start_time")
        end_times = request.POST.getlist("end_time")

        for i in range(len(days)):
            day = days[i]
            start = start_times[i]
            end = end_times[i]
            if day and start and end:
                Schedule.objects.create(
                    course=course,
                    day=day,
                    start_time=start,
                    end_time=end
                )

        return redirect("teacher_dashboard")

    # ✅ Lista de días para el template
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return render(request, "dashboard/edit_course.html", {
        "course": course,
        "schedules": schedules,
        "days": DAYS
    })


# Sessions

# NO se si esta es la real, creo que no
@login_required
def create_class_session(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)

    if request.method == "POST":
        course_id = request.POST.get("course")
        date_str = request.POST.get("date")
        topic = request.POST.get("topic")
        note = request.POST.get("note")

        if course_id and date_str:
            course = get_object_or_404(Course, id=course_id, teacher=teacher)
            date = parse_date(date_str)

            ClassSession.objects.create(
                course=course,
                date=date,
                topic=topic,
                note=note
            )
            return redirect("teacher_dashboard")

    return render(request, "dashboard/create_class_session.html", {
        "courses": courses
    })


@login_required
def create_class_session(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)

    course_id = request.GET.get("course")
    selected_course = None
    if course_id:
        selected_course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == "POST":
        course_id = request.POST.get("course")
        date = request.POST.get("date")
        topic = request.POST.get("topic")
        note = request.POST.get("note")

        if course_id and date:
            course = get_object_or_404(Course, id=course_id, teacher=teacher)
            ClassSession.objects.create(
                course=course,
                date=date,
                topic=topic,
                note=note
            )
            return redirect("course_sessions", course_id=course.id)

    return render(request, "dashboard/create_class_session.html", {
        "courses": courses,
        "selected_course": selected_course
    })


@login_required
def course_sessions(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)
    sessions = ClassSession.objects.filter(course=course)

    return render(request, "dashboard/course_sessions.html", {
        "course": course,
        "sessions": sessions
    })


@login_required
def edit_class_session(request, session_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(ClassSession, id=session_id, course__teacher=teacher)

    if request.method == "POST":
        session.date = request.POST.get("date")
        session.topic = request.POST.get("topic")
        session.note = request.POST.get("note")
        session.save()
        return redirect("course_sessions", course_id=session.course.id)

    return render(request, "dashboard/edit_class_session.html", {
        "session": session
    })


@login_required
def delete_class_session(request, session_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(ClassSession, id=session_id, course__teacher=teacher)
    course_id = session.course.id

    if request.method == "POST":
        session.delete()
        return redirect("course_sessions", course_id=course_id)

    return render(request, "dashboard/delete_class_session.html", {
        "session": session
    })


@login_required
def upload_material(request, session_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(ClassSession, id=session_id, course__teacher=teacher)

    if request.method == 'POST' and request.FILES.get('file'):
        Material.objects.create(session=session, file=request.FILES['file'])
        return redirect('course_sessions', course_id=session.course.id)

    return render(request, 'dashboard/upload_material.html', {
        'session': session
    })


@login_required
def delete_material(request, material_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    material = get_object_or_404(Material, id=material_id)
    session = material.session

    # Confirmar que el profesor es dueño del curso
    if session.course.teacher != teacher:
        return redirect("teacher_dashboard")

    if request.method == "POST":
        if material.file and os.path.isfile(material.file.path):
            os.remove(material.file.path)
        material.delete()

    return redirect("course_sessions", course_id=session.course.id)
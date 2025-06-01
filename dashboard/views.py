from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Teacher, ClassSession, Course, Schedule, Material, Student, Attendance, Grade, Observation
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Count, Q
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

    return render(request, "dashboard/auth/register.html")



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

    return render(request, "dashboard/auth/login.html")


def logout_teacher(request):
    logout(request)
    return redirect("login_teacher")



# Muestra todos los cursos del profesor
@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher).prefetch_related("schedules")

    return render(request, "dashboard/teacher_dashboard.html", {
        "teacher": teacher,
        "courses": courses
    })


# Crea un curso nuevo con múltiples horarios
@login_required
def create_course(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
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


# Edita un curso existente
@login_required
def edit_course(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)
    schedules = Schedule.objects.filter(course=course)

    if request.method == "POST":
        course.name = request.POST.get("name")
        course.description = request.POST.get("description", "")
        course.save()

        # Eliminar horarios anteriores y agregar nuevos
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

    # Lista de días de la semana
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return render(request, "dashboard/edit_course.html", {
        "course": course,
        "schedules": schedules,
        "days": DAYS
    })


# Elimina un curso
@login_required
def delete_course(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == "POST":
        course.delete()
        return redirect("teacher_dashboard")

    return render(request, "dashboard/delete_course.html", {"course": course})


# Sessions

# NO se si esta es la real, creo que no
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
            return redirect("course_detail", course_id=course.id)

    return render(request, "dashboard/create_class_session.html", {
        "courses": courses,
        "selected_course": selected_course
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
        return redirect("course_detail", course_id=session.course.id)

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
        return redirect("course_detail", course_id=course_id)

    return render(request, "dashboard/delete_class_session.html", {
        "session": session
    })


@login_required
def upload_material(request, session_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(ClassSession, id=session_id, course__teacher=teacher)

    if request.method == 'POST' and request.FILES.get('file'):
        Material.objects.create(session=session, file=request.FILES['file'])
        return redirect('course_detail', course_id=session.course.id)

    return render(request, "dashboard/upload_material.html", {"session": session})

@login_required
def delete_material(request, material_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    material = get_object_or_404(Material, id=material_id)
    session = material.session

    if session.course.teacher != teacher:
        return redirect("teacher_dashboard")

    if request.method == "POST":
        if material.file and os.path.isfile(material.file.path):
            os.remove(material.file.path)
        material.delete()

    return redirect("course_detail", course_id=session.course.id)


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()
    sessions = course.sessions.prefetch_related("attendances__student")

    return render(request, "dashboard/course_detail.html", {
        "course": course,
        "students": students,
        "sessions": sessions
    })



# Student´s logic

@login_required
def students_list(request):
    students = Student.objects.all().prefetch_related("courses")
    return render(request, "dashboard/student/all_students.html", {
        "students": students
    })


@login_required
def manage_students(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    students = Student.objects.filter(courses__in=courses).distinct()

    return render(request, "dashboard/student/manage_students.html", {
        "students": students,
        "courses": courses
    })


@login_required
def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course_ids = request.POST.getlist("courses")  # lista de cursos seleccionados

        if first_name and last_name and email:
            student, created = Student.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                }
            )
            for cid in course_ids:
                student.courses.add(cid)

            return redirect("students_list")

    courses = Course.objects.all()
    return render(request, "dashboard/student/add_student.html", {
        "courses": courses
    })


@login_required
def add_student_to_course(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if first_name and last_name and email:
            student, created = Student.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                },
            )
            student.courses.add(course)
            return redirect("course_detail", course_id=course.id)

    return render(request, "dashboard/student/add_student.html", {
        "course": course
    })


@login_required
def all_students(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher).prefetch_related('students')

    # Usamos un set para evitar duplicados si el mismo alumno está en varios cursos
    students = set()
    for course in courses:
        for student in course.students.all():
            students.add((student, course))

    return render(request, "dashboard/student/all_students.html", {
        "students": students
    })


@login_required
def delete_student(request, student_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, id=student_id)

    # Authorization: make sure the teacher is linked to at least one course of the student
    if not student.courses.filter(teacher=teacher).exists():
        return redirect("teacher_dashboard")

    if request.method == "POST":
        student.delete()
        return redirect("students_list")

    return redirect("students_list")


@login_required
def edit_student(request, student_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, id=student_id)
    courses = Course.objects.filter(teacher=teacher)

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")

        course_ids = request.POST.getlist("courses")
        student.courses.set(Course.objects.filter(id__in=course_ids, teacher=teacher))

        student.save()
        return redirect("students_list")

    return render(request, "dashboard/student/edit_student.html", {
        "student": student,
        "courses": courses
    })



@login_required
def remove_student_from_course(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, id=student_id)

    course.students.remove(student)

    return redirect('course_detail', course_id=course.id)


@login_required
def take_attendance(request, session_id):
    session = get_object_or_404(ClassSession, pk=session_id)
    students = session.course.students.all()

    if request.method == "POST":
        for student in students:
            present = request.POST.get(f'present_{student.id}') == 'on'
            justified = request.POST.get(f'justified_{student.id}') == 'on'
            Attendance.objects.update_or_create(
                class_session=session,
                student=student,
                defaults={'present': present, 'justified': justified}
            )
        return redirect('course_detail', course_id=session.course.id)

    return render(request, 'dashboard/student/take_attendance.html', {
        'session': session,
        'students': students
    })


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()
    sessions = course.sessions.prefetch_related("attendances__student")

    # Datos de asistencia por alumno
    students_stats = []
    total_sessions = course.sessions.count()

    for student in students:
        attendances = Attendance.objects.filter(class_session__course=course, student=student)

        present_count = attendances.filter(present=True).count()
        absent_count = attendances.filter(present=False).count()
        justified_absent = attendances.filter(present=False, justified=True).count()

        attendance_percent = round((present_count / total_sessions) * 100, 2) if total_sessions else 0

        students_stats.append({
            "student": student,
            "present": present_count,
            "absent": absent_count,
            "justified": justified_absent,
            "percent": attendance_percent
        })

    return render(request, "dashboard/course_detail.html", {
        "course": course,
        "students": students,
        "sessions": sessions,
        "students_stats": students_stats,
        "total_sessions": total_sessions
    })


@login_required
def add_observation(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Observation.objects.create(
                student=student,
                teacher=teacher,
                text=text
            )
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def add_grade(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        value = request.POST.get("value")
        description = request.POST.get("description", "")

        if value:
            Grade.objects.create(
                student=student,
                course=course,
                value=value,
                description=description
            )

    return redirect(request.META.get("HTTP_REFERER", "/"))
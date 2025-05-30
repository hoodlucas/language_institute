from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="courses")
    
    def __str__(self):
        return self.name


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="schedules")
    
    DAY_CHOICE = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.course.name} - {self.name}: {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"


class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    topic = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('course', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.course.name} - {self.date}"


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    courses = models.ManyToManyField(Course, related_name="students")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="attendances")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    present = models.BooleanField(default=False)
    justified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('class_session', 'student')
        
    def __str__(self):
        status = "Present" if self.present else "Absent"
        if not self.present and self.justified:
            status += " (Justified)"
        return f"{self.student} - {self.class_session.date} - {status}"


class Assigment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assigments")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_time = models.DateField()
    class_session = models.ForeignKey(ClassSession, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigments")
    
    def __str__(self):
        return f"{self.course.name} - {self.title}"


class AssigmentSubmission(models.Model):
    assigment = models.ForeignKey(Assigment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions")
    submited = models.BooleanField(default=False)
    submission_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('assigment', 'student')
    
    def __str__(self):
        return f"{self.student} - {self.assigment.title} - {'Submitted' if self.submited else 'Not submitted'}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    value = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.course.name}: {self.value}"

class Observation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="observations")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="observations")
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    
    def __str__(self):
        return f"{self.date} - {self.teacher.last_name} about {self.student}"


class Material(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='materials')
    file = models.FileField(upload_to='materials/', validators=[FileExtensionValidator(['pdf', 'docx', 'pptx', 'jpg', 'png'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name.split('/')[-1]
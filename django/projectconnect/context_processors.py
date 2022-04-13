from professors.models import Professor
from students.models import Student
from public_pages.models import HotJar

def add_professor_to_context(request):
    professor = None
    if request.user.is_authenticated:
        try:
            professor = Professor.objects.get(user=request.user)
        except:
            pass
    return { 'professor': professor }

def add_student_to_context(request):
    student = None
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
        except:
            pass
    return { 'student': student }

def add_hotjar_to_context(request):
    hotjar = HotJar.objects.get(id=1)
    hotjar.refresh_from_db()
    return { 'hotjar_script': hotjar.hotjar_script }
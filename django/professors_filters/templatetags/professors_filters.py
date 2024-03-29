from django import template
from professors.models import Professor, Course, Section, Project
from students.models import Student

register = template.Library()

############## Filters ###############
@register.filter
def courses_by_professor(professor):
    return Course.objects.filter(professor=professor)

@register.filter
def count_students_by_section(section):
    return len(section.students.all())

@register.filter
def count_projects_by_section(section):
    return len(section.projects.all())

############ Simple Tags #############

@register.simple_tag
def sections_by_course(course):
    return Section.objects.filter(course=course)

@register.simple_tag
def projects_by_course(course):
    return Project.objects.filter(course=course)

@register.simple_tag
def project_in_section(project, section):
    section.refresh_from_db()
    if project in section.projects.all():
        return True
    else:
        return False
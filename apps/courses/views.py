from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.text import slugify

from apps.accounts.permissions import instructor_required
from .models import Course, Lesson
from .forms import CourseForm, LessonForm
from apps.dashboard.models import CourseContent


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {
        'courses': courses
    })


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    content = CourseContent.objects(course_id=course.id).first()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'content': content
    })


@instructor_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('courses:add_lesson', course_id=course.id)
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})


@instructor_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # SECURITY CHECK: Ensure the logged-in user owns this course
    if course.instructor != request.user:
        return HttpResponseForbidden("You cannot add lessons to someone else's course.")

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('courses:add_lesson', course_id=course.id)
    else:
        form = LessonForm()

    # Get existing lessons to show a list below the form
    lessons = course.lessons.all()

    return render(request, 'courses/add_lesson.html', {
        'form': form,
        'course': course,
        'lessons': lessons
    })

    return render(request, 'dashboard/create_course.html')

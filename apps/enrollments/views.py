from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.courses.models import Course, Lesson
from .models import Enrollment, LessonProgress
from django.utils import timezone


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    return redirect('course_detail', course_id=course.id)


@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson
    )
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    return redirect('lesson_detail', lesson_id=lesson.id)

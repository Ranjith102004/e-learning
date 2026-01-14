from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.courses.models import Course
from .models import Enrollment
from django.utils import timezone
from apps.dashboard.models import CourseContent, StudentProgress
import datetime


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    # Ensure a StudentProgress document exists for this user and course
    sp = StudentProgress.objects(user_id=request.user.id, course_id=course.id).first()
    if not sp:
        StudentProgress(
            user_id=request.user.id,
            course_id=course.id,
            completed_lessons=[],
            progress_percent=0
        ).save()

    return redirect('course_detail', course_id=course.id)


@login_required
def complete_lesson(request, lesson_id):
    # Locate the course content that contains this lesson
    content = CourseContent.objects(modules__lessons__lesson_id=lesson_id).first()
    if not content:
        return redirect('courses:list')

    course_id = content.course_id

    sp = StudentProgress.objects(user_id=request.user.id, course_id=course_id).first()
    if not sp:
        sp = StudentProgress(user_id=request.user.id, course_id=course_id, completed_lessons=[], progress_percent=0)

    if lesson_id not in sp.completed_lessons:
        sp.completed_lessons.append(lesson_id)
        # calculate total lessons for progress percent
        total_lessons = 0
        for m in content.modules:
            total_lessons += len(m.lessons)
        sp.progress_percent = int((len(sp.completed_lessons) / total_lessons) * 100) if total_lessons else 0
        sp.last_updated = datetime.datetime.utcnow()
        sp.save()

    return redirect('lesson_detail', lesson_id=lesson_id)

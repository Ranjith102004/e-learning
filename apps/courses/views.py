from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Course
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


@login_required
def create_course(request):
    if not getattr(request.user, 'is_instructor', False):
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        slug = slugify(title)
        category = request.POST.get('category', 'Programming')
        level = request.POST.get('level', 'beginner')

        course = Course.objects.create(
            instructor=request.user,
            title=title,
            slug=slug,
            category=category,
            level=level,
            price=price,
            is_published=True
        )

        # create empty CourseContent document in Mongo
        CourseContent(course_id=course.id, modules=[]).save()

        return redirect('dashboard')

    return render(request, 'dashboard/create_course.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {
        'courses': courses
    })


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # lessons belonging to the course via modules
    lessons = Lesson.objects.filter(module__course=course)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons
    })


@login_required
def create_course(request):
    if request.user.role != 'instructor':
        return redirect('home')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']

        Course.objects.create(
            instructor=request.user,
            title=title,
            description=description,
            price=price,
            is_published=True
        )
        return redirect('dashboard')

    return render(request, 'dashboard/create_course.html')

from django.shortcuts import render, redirect
from decimal import Decimal

from apps.accounts.permissions import instructor_required
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from apps.dashboard.mongo_models import CourseContent


@instructor_required
def instructor_dashboard(request):
    courses_qs = Course.objects.filter(instructor=request.user)

    data = []
    for c in courses_qs:
        students = Enrollment.objects.filter(course=c).count()
        revenue = (c.price or Decimal('0')) * students
        data.append({
            'course': c,
            'students': students,
            'revenue': revenue
        })

    return render(
        request,
        'dashboard/instructor_dashboard.html',
        {'courses': data}
    )


@instructor_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price') or 0

        course = Course.objects.create(
            instructor=request.user,
            title=title,
            slug=title.lower().replace(' ', '-'),
            category='Programming',
            level='beginner',
            price=price,
            is_published=True
        )

        # create empty Mongo content
        CourseContent.objects.create(
            course_id=course.id,
            modules=[]
        )

        return redirect('dashboard:dashboard')

    return render(request, 'dashboard/create_course.html')

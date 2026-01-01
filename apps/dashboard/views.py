from django.shortcuts import render, redirect
from apps.accounts.permissions import instructor_required
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from decimal import Decimal


@instructor_required
def instructor_dashboard(request):
    courses_qs = Course.objects.all()  # later filter by instructor

    data = []
    for c in courses_qs:
        students = Enrollment.objects.filter(course=c).count()
        revenue = (c.price or Decimal('0')) * students
        data.append({'course': c, 'students': students, 'revenue': revenue})

    return render(request, 'dashboard/instructor_dashboard.html', {
        'courses': data
    })


@instructor_required
def create_course(request):
    if request.method == 'POST':
        Course.objects.create(
            instructor=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price') or 0
        )

        return redirect('dashboard')

    return render(request, 'dashboard/create_course.html')

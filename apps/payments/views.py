from django.shortcuts import render, get_object_or_404
from apps.courses.models import Course


def checkout(request):
    course_id = request.GET.get('course_id')
    if course_id:
        course = get_object_or_404(Course, id=course_id)
    else:
        course = {'title': 'Sample Course', 'price': 499}

    return render(request, 'payments/checkout.html', {
        'course': course
    })


def success(request):
    return render(request, 'payments/success.html')


def cancel(request):
    return render(request, 'payments/cancel.html')

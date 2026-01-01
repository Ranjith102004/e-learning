from django.urls import path
from .views import enroll_course, complete_lesson

urlpatterns = [
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('complete/<int:lesson_id>/', complete_lesson, name='complete_lesson'),
]

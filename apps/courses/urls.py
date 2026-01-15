from django.urls import path
from .views import course_list, course_detail, create_course, add_lesson

app_name = 'courses'

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<int:course_id>/', course_detail, name='course_detail'),
    path('create/', create_course, name='create'),
    path('<int:course_id>/add-lesson/', add_lesson, name='add_lesson'),
]

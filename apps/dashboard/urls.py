from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.instructor_dashboard, name='dashboard'),
    path('create-course/', views.create_course, name='create_course'),
]
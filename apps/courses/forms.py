from django import forms
from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'thumbnail', 'category', 'level']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video', 'order', 'duration']

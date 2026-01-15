
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    is_instructor = forms.BooleanField(
        required=False, 
        label="Register as Instructor",
        help_text="Check this if you want to create courses."
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_instructor']:
            user.role = User.Role.INSTRUCTOR
        else:
            user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    pass
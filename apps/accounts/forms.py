# apps/accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    # Add the checkbox that we saw in your register.html
    is_instructor = forms.BooleanField(
        required=False, 
        label="Register as Instructor",
        help_text="Check this if you want to create courses."
    )

    class Meta:
        model = User
        fields = ('username', 'email')  # Password is included automatically

    def save(self, commit=True):
        # 1. Get the user instance but don't save to DB yet
        user = super().save(commit=False)
        
        # 2. Set the role based on the checkbox
        if self.cleaned_data['is_instructor']:
            user.role = User.Role.INSTRUCTOR # Uses the choices from your updated models.py
        else:
            user.role = User.Role.STUDENT
            
        # 3. Save the user to the DB
        if commit:
            user.save()
        return user


# We can use the standard AuthenticationForm for login, 
# but you can subclass it here if you ever need custom logic.
class UserLoginForm(AuthenticationForm):
    pass

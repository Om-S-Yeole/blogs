from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(min_value=0, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password1', 'password2']
    
    def save(self, commit=True):
        # Call the parent class's save method to get the User instance
        user = super().save(commit=False)
        # Save additional fields (email, first_name, last_name)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()  # Save the User object to the database
            # Save the Profile instance
            Profile.objects.create(user=user, age=self.cleaned_data.get('age'))
        return user
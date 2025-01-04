from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(min_value=0, required=False)
    subscription_preference = forms.BooleanField(required=False, label="Hey Om, I would also like to get your weekly insights through weekly emails.")
    terms_and_privacy_policy_acceptance = forms.BooleanField(required=True, label="By registering for new account, I accept the Terms and Conditions and Privacy Policies.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password1', 'password2', 'subscription_preference', 'terms_and_privacy_policy_acceptance']
    
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
            Profile.objects.create(user=user,
                                age=self.cleaned_data.get('age'),
                                subscription_preference=self.cleaned_data.get('subscription_preference'),
                                terms_and_privacy_policy_acceptance = self.cleaned_data.get('terms_and_privacy_policy_acceptance'))
        return user
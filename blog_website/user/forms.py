from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .utils import account_activation_token  # Import the token generator
from django.core.mail import send_mail

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(min_value=0, required=False)
    subscription_preference = forms.BooleanField(required=False, label="Hey Om, I would also like to get your weekly insights through weekly emails.")
    terms_and_privacy_policy_acceptance = forms.BooleanField(required=True, label="By registering for a new account, I accept the Terms and Conditions and Privacy Policy.")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password1', 'password2', 'subscription_preference', 'terms_and_privacy_policy_acceptance']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_active = False  # Mark user as inactive until email verification

        if commit:
            user.save()
            # Save additional fields in the Profile model
            Profile.objects.create(
                user=user,
                age=self.cleaned_data.get('age'),
                subscription_preference=self.cleaned_data.get('subscription_preference'),
                terms_and_privacy_policy_acceptance=self.cleaned_data.get('terms_and_privacy_policy_acceptance')
            )
            # Send verification email
            self.send_verification_email(user)

        return user

    def send_verification_email(self, user):
        subject = 'Verify Your Email Address'
        message = render_to_string('user/email_verification.html', {
            'user': user,
            'domain': 'localhost:8000/',  # Replace with your domain
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    age = forms.IntegerField(min_value=0, required=True)
    subscription_preference = forms.BooleanField(required=False, label="Hey Om, I would also like to get your weekly insights through weekly emails.")

    class Meta:
        model = User
        fields = ['age', 'subscription_preference']
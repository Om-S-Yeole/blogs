from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from .utils import account_activation_token
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

def register(request):
    form = None
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and the profile together
            user = form.save(commit=True)

            # Send activation email
            send_activation_email(user, request)

            messages.success(
                request,
                f"Your account has been created! Please check your email to verify your account before logging in."
            )
            return redirect("login")
        else:
            # Handle invalid form submission
            messages.warning(request, f"Please correct the errors in the form.")
            return redirect("register")
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'title': 'Register',
    }
    return render(request, 'user/register.html', context)


def send_activation_email(user, request):
    subject = 'Verify Your Email Address'
    # Generate UID and token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    # Get the domain of the current site
    domain = get_current_site(request).domain

    # Generate the activation link
    activation_link = reverse('activate-account', kwargs={'uidb64': uid, 'token': token})

    # Construct the full URL for the email
    activation_url = f"http://{domain}{activation_link}"

    # Email message context
    message = render_to_string('user/email_verification.html', {
        'user': user,
        'activation_link': activation_url,
    })

    # Send the email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def activate_account(request, uidb64, token):
    try:
        # Decode the UID and get the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Activate the user's account
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified! You can now log in.")
        return redirect("login")
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect("register")

class CustomLoginView(LoginView):
    template_name = "user/login.html"  # Specify the template name

    def get_context_data(self, **kwargs):
        # Call the parent method to get the default context
        context = super().get_context_data(**kwargs)
        # Add your custom context
        context['title'] = "Login to Your Account"
        return context
    

@login_required
def subscribe(request):
    if request.method == "POST":
        user = request.user
        user.profile.subscription_preference = True
        user.profile.save()
        return JsonResponse({"message": "Subscription successful!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def profile(request):
    context = {
        'title': f"{request.user}'s Profile",
    }
    return render(request, 'user/profile.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        u_form.is_valid()
        if ((User.objects.filter(email=u_form.cleaned_data.get('email')).exists()) and (User.objects.filter(email=u_form.cleaned_data.get('email')).first().username != request.user.username)):
            messages.warning(request, f"This email is already registered. Please use a different email.")
            return redirect("profile_update")

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your Account has been Updated.")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': "Update Your Profile",
    }

    return render(request, 'user/profile_update.html', context)
    
class Delete_account(LoginRequiredMixin, DeleteView):
    model = User
    success_url = "/"
    template_name = "user/user_confirm_delete.html"  # Path to your custom template

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user
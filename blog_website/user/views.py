from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView

def register(request):
    form = None
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        form.is_valid()
        if User.objects.filter(email=form.cleaned_data.get('email')).exists():
            messages.warning(request, f"This email is already registered. Please use a different email.")
            return redirect("register")
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Your Account has been created. You are now able to Login")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'title': 'Register',
    }
    return render(request, 'user/register.html', context)

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
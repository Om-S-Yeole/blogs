from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView

def register(request):
    form = None
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Your Account has been created. You are now able to Login")
            return redirect("blog-home")
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
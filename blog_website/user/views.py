from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages

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
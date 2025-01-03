from django.shortcuts import render

def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'blog/home.html', context)

def about_me(request):
    context = {
        'title': 'About Me',
    }
    return render(request, 'blog/about_me.html', context)

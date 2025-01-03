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

def contact_us(request):
    context = {
        'title': 'Contact Us',
    }
    return render(request, 'blog/contact_us.html', context)
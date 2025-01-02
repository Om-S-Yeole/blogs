from django.shortcuts import render

def home(request):
    context = {
        'title': 'My Title 1',
    }
    return render(request, 'blog/home.html', context)

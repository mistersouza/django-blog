from django.shortcuts import render
from .models import About
# Views
def about_me(request):
    about = About.objects.all().order_by('-updated_on').first()
    context = {
        'about': about
    }

    return render(request, 'about/about.html', context)
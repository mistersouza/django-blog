from django.shortcuts import render
from .models import About, CollaborateRequest
from .forms import CollaborateForm

# Views
def about_me(request):
    about = About.objects.all().order_by('-updated_on').first()
    collaborate_form = CollaborateForm()

    context = {
        'about': about,
        'collaborate_form': collaborate_form
    }

    return render(request, 'about/about.html', context)
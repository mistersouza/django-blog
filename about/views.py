from django.shortcuts import render
from django.contrib import messages
from .models import About, CollaborateRequest
from .forms import CollaborateForm

# Views
def about_me(request):
    about = About.objects.all().order_by('-updated_on').first()

    if request.method == 'POST':
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Collaboration request received! I endeavour to respond within 2 working days.'
            )
    
    collaborate_form = CollaborateForm();  

    context = {
        'about': about,
        'collaborate_form': collaborate_form
    }

    return render(request, 'about/about.html', context)
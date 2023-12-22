from django.shortcuts import render
from django.contrib import messages
from .models import About, CollaborateRequest
from .forms import CollaborateForm


# Views
def about_me(request):
    """
    Display the 'About Me' page and handle collaboration requests.

    **Behavior**

    Retrieves the latest 'About' instadce of :model:`about.about`.
    Processes POST requests to handle collaboration form submissions.
    Renders the 'about.html' template with 'About' information and
    the collaboration form.

    **Context**

    ``About``
        The most recent instance of :model:`about.about`.

    ``collaborate_form``
        An instance of :form:`about.CollaborateForm`.

    :template:`about/about.html`
    """
    about = About.objects.all().order_by('-updated_on').first()

    if request.method == 'POST':
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Collaboration request received!'
            )

    collaborate_form = CollaborateForm()

    context = {
        'about': about,
        'collaborate_form': collaborate_form
    }

    return render(request, 'about/about.html', context)

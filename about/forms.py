from django import forms
from .models import CollaborateRequest


class CollaborateForm(forms.ModelForm):
    """
    Form used for capturing collaboration requests through a web interface.
    """
    class Meta:
        model = CollaborateRequest
        fields = ('name', 'email', 'message',)

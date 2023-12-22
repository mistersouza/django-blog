from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating or updating a :model:`blog.Comment`.

    **Attributes:**

    ``model``
        Specifies the model associated with the form.

    ``fields``
        Fields to be included in the form.
    """

    class Meta:
        """
        Metadata class for the CommentForm.
        """
        model = Comment
        fields = ('body',)

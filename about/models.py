from django.db import models
from cloudinary.models import CloudinaryField


# Models
class About(models.Model):
    """
    Model to store information about the website's About section.
    """
    title = models.CharField()
    profile_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now_add=True)

    # Returns the title of the About section as a string.
    def __str__(self):
        return self.title


class CollaborateRequest(models.Model):
    """
    Model to handle collaboration requests received through the website.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    # Returns a string of request with the requester's name.
    def __str__(self):
        return f"Collaboration request from {self.name}"

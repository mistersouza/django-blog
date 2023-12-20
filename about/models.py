from django.db import models

# Models
class About(models.Model):
    title = models.CharField()
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

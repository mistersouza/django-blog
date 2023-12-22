from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


# Models
class Post(models.Model):
    """
    Stores a single blog post entry related to a user (:model:`auth.User`).

    Related field:
        author (ForeignKey to :model:`auth.User`): The author of the post.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

    # Sets ordering option,
    # arranging posts by creation date in descending order
    class Meta:
        ordering = ["-created_on"]

    # Returns a string representation of the Post instance.
    def __str__(self):
        return f'{self.title} | written by {self.author.first_name}'


class Comment(models.Model):
    """
    Stores single comments entry related to :model:`auth.User`
    and :model:`blog.Post`

    Related fields:
        author (ForeignKey to :model:`auth.User`): The author of the post.
        author (ForeignKey to :model:`auth.User`): The commenter.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    # Sets ordering option,
    # arranging posts by creation date in descending order
    class Meta:
        ordering = ["created_on"]

    # Returns a string representation of the comment instance.
    def __str__(self):
        return f"Comment {self.body} by {self.author}"

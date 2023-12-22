from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm


# Views
class PostList(generic.ListView):
    """
    Display a list of published :model:`blog.Post` instances.

    **Attributes:**

    ``queryset``
        Filters the list to display only published posts.

    ``template_name``
        The template used to render the view.

    ``paginate_by``
        Number of posts per page for pagination.
    """
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    render a single post :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    ``comments``
        All comments related to the displayed post, ordered by creation date.

    ``comment_count``
        Count of approved comments related to the displayed post.

    ``comment_form``
        An instance of :class:`blog.forms.CommentForm` to submit a new comment.

    **Template**
    :template:`blog/post_detail.html`

    :param request: HttpRequest object
    :param slug: Slug of the post to be displayed
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        # populate form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object only
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
    # reset form, ready to use again
    comment_form = CommentForm()

    context = {
        "post": post,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form,
        }

    return render(request, "blog/post_detail.html", context)


def comment_edit(request, slug, comment_id):
    """
    Edit comments related to a specific :model:`blog.Post`.

    **Behavior**

    On a POST request, attempts to edit the specified comment
    associated with the given post. If the comment's author matches
    the logged-in user and the form is valid, updates the comment.
    Otherwise, raises an error message indicating an issue with the update.

    Redirects to the 'post_detail' view for the specific post.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    ``comment``
        An instance of :model:`blog.Comment` to be edited.

    ``comment_form``
        An instance of :class:`blog.forms.CommentForm` to edit the comment.

    :param request: HttpRequest object
    :param slug: Slug of the post related to the comment
    :param comment_id: ID of the comment to be edited
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS,
                'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Delete a specific comment related to a :model:`blog.Post`.

    **Behavior**

    Checks if the logged-in user is the author of the comment to be deleted.
    If so, deletes the comment; otherwise, raises an error message
    indicating that only the author can delete their own comment.

    Redirects to the 'post_detail' view of specific post after deletion.

    :param request: HttpRequest object
    :param slug: Slug of the post related to the comment
    :param comment_id: ID of the comment to be deleted
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS,
            'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR,
            'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

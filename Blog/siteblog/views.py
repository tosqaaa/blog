from Blog.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import EmailPostForm, CommentPostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.publish.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, published__year=year, published__month=month, published__day=day,
                             status=Post.Status.PUBLISHED)

    comments = post.comments.filter(active=True)
    form = CommentPostForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, template_name='blog/post/post_detail.html', context=context)


def email_share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            messages.success(request, "Форма отправлена успешно!")
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleaned_data['name']} ({cleaned_data['email_from']}) Рекомендует прочитать пост"
            message = (f"Прочитай '{post.title}' по ссылке {post_url} "
                       f"Комментарии: {cleaned_data['comments']}")

            send_mail(subject, message, EMAIL_HOST_USER, (cleaned_data['email_to'],))
        else:
            messages.error(request, f"Ошибка отправки формы {form.errors}")
    else:
        form = EmailPostForm()

    print(form.as_p())

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post/email_share_post.html', context=context)


@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentPostForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, "Комментарий успешно оставлен!")
    else:
        form = CommentPostForm()
        messages.error(request, 'Ошибка комментария!')
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'blog/post/comment.html', context=context)

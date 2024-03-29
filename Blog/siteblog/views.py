from Blog.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentPostForm, SearchForm
from .models import Post


class PostListView(ListView):
    queryset = Post.publish.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            context['tag'] = get_object_or_404(Tag, slug=slug)
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            tag = get_object_or_404(Tag, slug=slug)
            return Post.publish.filter(tags__in=[tag])
        return Post.publish.all()


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, published__year=year, published__month=month, published__day=day,
                             status=Post.Status.PUBLISHED)

    comments = post.comments.filter(active=True)
    form = CommentPostForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.publish.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')[:4]
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
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


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.publish.annotate(similarity=TrigramSimilarity('title', query), ).filter(
                similarity__gt=0.1).order_by('-similarity')
        else:
            print(form.errors())
    context = {
        'form': form,
        'query': query,
        'results': results
    }
    return render(request, 'blog/post/search.html', context=context)

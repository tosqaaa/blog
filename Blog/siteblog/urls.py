from django.urls import path

from .views import PostListView, post_detail, email_share_post, comment_post, post_search

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('tag/<slug:slug>', PostListView.as_view(), name='post_tag'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>', post_detail, name='post_detail'),
    path('email_send_post/<int:post_id>', email_share_post, name='email_share_post'),
    path('comment/<int:post_id>', comment_post, name='comment_post'),
    path('post/search', post_search, name='post_search'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(arg=('siteblog.urls', 'blog'), namespace='blog')),
]

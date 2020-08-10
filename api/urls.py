from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('posts/', include('api.posts.urls'))
]
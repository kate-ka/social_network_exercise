from django.urls import path

from api.posts import views
from api.posts.views import LikeListView

urlpatterns = [
    path('', views.ListCreatePostView.as_view()),
    path('<int:pk>/', views.RetrievePostView.as_view()),
    path('like/<int:post_id>/', views.LikePostView.as_view()),
    path('unlike/<int:post_id>/', views.UnlikePostView.as_view()),
    path('analytics/', LikeListView.as_view()),
]


from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticlesAPIView.as_view(), name='articles'),
    path('articles/<int:id>/', views.OneArticleAPIView, name='article'),
    path('articles/<int:id>/comments/', views.ArticleCommentsAPIView, name='comments'),
    path('create_comment/', views.CreateCommentAPIView.as_view(), name='create_comment'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]

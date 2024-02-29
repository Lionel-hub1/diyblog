from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]

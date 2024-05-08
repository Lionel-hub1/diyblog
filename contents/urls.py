from django.urls import path, include
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DIY Blog API",
        default_version='v1',
        description="My API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('articles/', views.ArticlesAPIView.as_view(), name='articles'),
    path('articles/<int:id>/', views.OneArticleAPIView, name='article'),
    path('articles/<int:id>/comments/',
         views.ArticleCommentsAPIView, name='comments'),
    path('create_comment/', views.CreateCommentAPIView.as_view(),
         name='create_comment'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]

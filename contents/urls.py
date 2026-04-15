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
    path('articles/<int:id>/', views.OneArticleAPIView.as_view(), name='article'),
    path('types/', views.TypeListCreateAPIView.as_view(), name='types'),
    path('types/<int:id>/', views.TypeDetailAPIView.as_view(), name='type-detail'),
    path('articles/upload-image/',
         views.RichTextImageUploadAPIView.as_view(), name='article-upload-image'),
    path('articles/<int:id>/comments/',
         views.ArticleCommentsAPIView.as_view(), name='comments'),
    path('comments/<int:id>/', views.CommentDetailAPIView.as_view(),
         name='comment-detail'),
    path('create_comment/', views.CreateCommentAPIView.as_view(),
         name='create_comment'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]

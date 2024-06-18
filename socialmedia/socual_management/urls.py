from django.urls import path
from .views import SignUpView, LoginView, PostCreateAPIView, PostLikeAPIView, PostUnlikeAPIView, PostListAPIView,ImageUploadView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/<int:post_id>/like/', PostLikeAPIView.as_view(), name='post-like'),
    path('posts/<int:post_id>/unlike/', PostUnlikeAPIView.as_view(), name='post-unlike'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    # Add more URLs as needed for other CRUD operations or additional features
]

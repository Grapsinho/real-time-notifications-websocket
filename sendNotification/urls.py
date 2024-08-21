from django.urls import path
from .views import PostListView, PostDetailView, AddCommentView, get_notifications

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('notifications/', get_notifications, name='get-notifications'),
]
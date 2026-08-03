from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AssignedToMeView,
    CommentDeleteView,
    CommentListCreateView,
    ReviewingView,
    TaskViewSet,
)

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(),
         name='tasks-assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='tasks-reviewing'),
    path('tasks/<int:task_id>/comments/',
         CommentListCreateView.as_view(), name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/',
         CommentDeleteView.as_view(), name='task-comment-delete'),
] + router.urls

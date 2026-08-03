from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks_app.models import Comment, Task

from .permissions import (IsBoardMemberForTask,IsCommentAuthor,IsTaskBoardMember,IsTaskCreatorOrBoardOwner)
from .serializers import (CommentCreateSerializer,CommentSerializer,TaskCreateSerializer,TaskSerializer,TaskUpdateSerializer)


class AssignedToMeView(generics.ListAPIView):
    """Lists tasks where the requesting user is the assignee."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks assigned to the requesting user."""
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    """Lists tasks where the requesting user is the reviewer."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks where the requesting user is the reviewer."""
        return Task.objects.filter(reviewer=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """Handles creating, updating and deleting tasks."""

    queryset = Task.objects.all()
    http_method_names = ['post', 'patch', 'delete']

    def get_serializer_class(self):
        """Select the serializer class based on the current action."""
        if self.action == 'create':
            return TaskCreateSerializer
        if self.action == 'partial_update':
            return TaskUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        """Select permission classes based on the current action."""
        if self.action == 'create':
            return [IsAuthenticated(), IsBoardMemberForTask()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsTaskBoardMember()]

    def create(self, request, *args, **kwargs):
        """Create a task and return it with full details."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Update a task and return it with full details."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskSerializer(task).data)


class CommentListCreateView(generics.ListCreateAPIView):
    """Lists and creates comments for a specific task."""

    permission_classes = [IsAuthenticated, IsTaskBoardMember]

    def get_task(self):
        """Fetch the task from the URL and check object permissions on it."""
        task = generics.get_object_or_404(Task, id=self.kwargs['task_id'])
        self.check_object_permissions(self.request, task)
        return task

    def get_queryset(self):
        """Return all comments belonging to the task from the URL."""
        return self.get_task().comments.all()

    def get_serializer_class(self):
        """Select the serializer class based on the request method."""
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_serializer_context(self):
        """Add the task to the serializer context for comment creation."""
        context = super().get_serializer_context()
        context['task'] = self.get_task()
        return context

    def create(self, request, *args, **kwargs):
        """Create a comment and return it with full details."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
    """Deletes a specific comment from a task."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_object(self):
        """Fetch the comment scoped to the task from the URL."""
        comment = generics.get_object_or_404(
            Comment, id=self.kwargs['comment_id'], task_id=self.kwargs['task_id']
        )
        self.check_object_permissions(self.request, comment)
        return comment

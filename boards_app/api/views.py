from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boards_app.models import Board

from .permissions import IsBoardMemberOrOwner, IsBoardOwner
from .serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardListSerializer,
    BoardUpdateResponseSerializer,
    BoardUpdateSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    """Handles listing, creating, retrieving, updating and deleting boards."""

    def get_queryset(self):
        """Return only owned/member boards for list; all boards otherwise."""
        if self.action == 'list':
            user = self.request.user
            return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        return Board.objects.all()

    def get_serializer_class(self):
        """Select the serializer class based on the current action."""
        serializer_map = {
            'list': BoardListSerializer,
            'create': BoardCreateSerializer,
            'retrieve': BoardDetailSerializer,
            'update': BoardUpdateSerializer,
            'partial_update': BoardUpdateSerializer,
        }
        return serializer_map.get(self.action, BoardListSerializer)

    def get_permissions(self):
        """Select permission classes based on the current action."""
        if self.action == 'destroy':
            return [IsAuthenticated(), IsBoardOwner()]
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsBoardMemberOrOwner()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create a board and return it in the list response format."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response(BoardListSerializer(board).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update a board and return it with full owner and member details."""
        instance = self.get_object()
        partial = kwargs.get('partial', False)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response(BoardUpdateResponseSerializer(board).data)

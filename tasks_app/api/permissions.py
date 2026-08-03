from rest_framework.permissions import BasePermission

from boards_app.models import Board


class IsBoardMemberForTask(BasePermission):
    """Allows task creation only if the user is a member or owner of the target board."""

    def has_permission(self, request, view):
        """Check board membership using the board id from the request data."""
        if request.method != 'POST':
            return True
        board_id = request.data.get('board')
        if not board_id:
            return True  # let the serializer report the missing field as 400
        try:
            board = Board.objects.get(id=board_id)
        except (Board.DoesNotExist, ValueError, TypeError):
            return True  # let the serializer report the invalid id as 400
        return request.user == board.owner or board.members.filter(id=request.user.id).exists()


class IsTaskBoardMember(BasePermission):
    """Allows access only to members or the owner of the task's board."""

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is a member or owner of the task's board."""
        board = obj.board
        return request.user == board.owner or board.members.filter(id=request.user.id).exists()


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allows deletion only to the task's creator or the board's owner."""

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user created the task or owns its board."""
        return request.user == obj.owner or request.user == obj.board.owner


class IsCommentAuthor(BasePermission):
    """Allows deletion only to the comment's author."""

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is the comment's author."""
        return request.user == obj.author

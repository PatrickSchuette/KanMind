from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """Allows access only to a board's owner or one of its members."""

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is the owner or a member."""
        return request.user == obj.owner or request.user in obj.members.all()


class IsBoardOwner(BasePermission):
    """Allows access only to a board's owner."""

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is the owner."""
        return request.user == obj.owner

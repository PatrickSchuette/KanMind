from django.contrib.auth.models import User
from rest_framework import serializers

from tasks_app.models import Comment, Task
from datetime import date

class UserNestedSerializer(serializers.ModelSerializer):
    """Represents a user with id, email and fullname for nested task data."""

    fullname = serializers.CharField(source='profile.fullname')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskNestedSerializer(serializers.ModelSerializer):
    """Represents a task nested inside a board's detail view."""

    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority','assignee', 'reviewer', 'due_date', 'comments_count']        

    def get_comments_count(self, obj):
        """Return the number of comments on this task."""
        
        return obj.comments.count()


class TaskSerializer(serializers.ModelSerializer):
    """Represents a task with full details, used for create/update responses."""

    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority','assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Return the number of comments on this task."""
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Validates data for creating a new task."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority','assignee_id', 'reviewer_id', 'due_date']

    def validate(self, attrs):
        """Ensure assignee and reviewer are members of the board."""
        
        board = attrs.get('board')
        for role in ['assignee', 'reviewer']:
            user = attrs.get(role)
            if user and not self._is_board_member(board, user):
                raise serializers.ValidationError(f'{role} must be a member of the board.')
        return attrs

    def _is_board_member(self, board, user):
        """Check whether the given user is a member or owner of the board."""
        
        return user == board.owner or board.members.filter(id=user.id).exists()

    def create(self, validated_data):
        """Create the task with the requesting user as owner."""
        
        owner = self.context['request'].user
        return Task.objects.create(owner=owner, **validated_data)
    
    def validate_due_date(self, value):
        """Ensure the due date is not in the past."""
        
        if value and value < date.today():
            raise serializers.ValidationError('Due date cannot be in the past.')
        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Validates data for updating an existing task. The board cannot be changed."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority','assignee_id', 'reviewer_id', 'due_date']

    def validate(self, attrs):
        """Ensure assignee and reviewer are members of the task's board."""
        
        board = self.instance.board
        for role in ['assignee', 'reviewer']:
            user = attrs.get(role)
            if user and not self._is_board_member(board, user):
                raise serializers.ValidationError(f'{role} must be a member of the board.')
        return attrs

    def _is_board_member(self, board, user):
        """Check whether the given user is a member or owner of the board."""
        
        return user == board.owner or board.members.filter(id=user.id).exists()


class CommentSerializer(serializers.ModelSerializer):
    """Represents a comment with author fullname and content."""

    author = serializers.CharField(
        source='author.profile.fullname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']


class CommentCreateSerializer(serializers.ModelSerializer):
    """Validates data for creating a new comment."""

    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        """Create the comment with the requesting user as author and the given task."""
        
        return Comment.objects.create(
            task=self.context['task'],
            author=self.context['request'].user,
            **validated_data,
        )

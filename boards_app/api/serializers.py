from django.contrib.auth.models import User
from rest_framework import serializers

from tasks_app.api.serializers import TaskNestedSerializer
from boards_app.models import Board


class UserNestedSerializer(serializers.ModelSerializer):
    """Represents a user with id, email and fullname for nested board data."""

    fullname = serializers.CharField(source='profile.fullname')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskNestedSerializer(serializers.Serializer):
    """Represents a task nested inside a board's detail view."""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    priority = serializers.CharField()
    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)
    due_date = serializers.DateField()
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        """Return the number of comments on this task."""
        
        return obj.comments.count()


class BoardListSerializer(serializers.ModelSerializer):
    """Represents a board in list view and as the create response."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count','tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        """Return the number of members on this board."""
        
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return the total number of tasks on this board."""
        
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Return the number of tasks with status 'to-do'."""
        
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Return the number of tasks with priority 'high'."""
        
        return obj.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    """Validates data for creating a new board."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'members']

    def create(self, validated_data):
        """Create the board with the requesting user as owner."""
        
        members = validated_data.pop('members', [])
        owner = self.context['request'].user
        board = Board.objects.create(owner=owner, **validated_data)
        board.members.set(members)
        return board


class BoardDetailSerializer(serializers.ModelSerializer):
    """Represents a board with full member and task details."""

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = UserNestedSerializer(many=True, read_only=True)
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(serializers.ModelSerializer):
    """Validates data for updating a board's title and members."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'members']

    def update(self, instance, validated_data):
        """Update the title and replace the board's members."""
        
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        if 'members' in validated_data:
            instance.members.set(validated_data['members'])
        return instance


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    """Represents a board after update, with full owner and member details."""

    owner_data = UserNestedSerializer(source='owner', read_only=True)
    members_data = UserNestedSerializer(
        source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data']

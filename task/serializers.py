from rest_framework import serializers
from extauth.models import ExtendedUser
from models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user.username')

    class Meta:
        model = TaskResult
        fields = ('id', 'input_param', 'status', 'result', 'user', 'created_at', 'resulted_at')


class ExtendedUserSerializer(serializers.ModelSerializer):
    task_results = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = ExtendedUser
        fields = ('id', 'username', 'task_results')

from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=True)
    description = serializers.CharField(required=True)
    duration = serializers.IntegerField(required=True)

    class Meta:
        model = Task
        fields = "__all__"

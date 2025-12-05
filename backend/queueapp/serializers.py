from rest_framework import serializers
from queueapp.models import QueueEntry


class QueueEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueEntry
        fields = ['id', 'patient', 'consultation', 'status', 'joined_at', 'served_at']
        read_only_fields = ['id', 'status', 'joined_at', 'served_at']

import uuid
from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'patient', 'amount', 'status', 'transaction_code', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'transaction_code', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['transaction_code'] = uuid.uuid4().hex
        return super().create(validated_data)


class PaymentProcessSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approve", "fail"])

    def update(self, instance, validated_data):
        action = validated_data["action"]
        instance.status = Payment.STATUS_PAID if action == "approve" else Payment.STATUS_FAILED
        instance.save()
        return instance

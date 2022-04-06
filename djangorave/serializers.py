# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from rest_framework import serializers

# project imports
from djangorave.models import TransactionModel, PaymentTypeModel


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the Transaction Model"""

    tx_ref = serializers.CharField(source="reference")
    flw_ref = serializers.CharField(source="flutterwave_reference")
    orderRef = serializers.CharField(source="order_reference")

    class Meta:
        model = TransactionModel
        fields = ("tx_ref", "flw_ref", "orderRef", "amount", "charged_amount", "status")

    def validate_reference(self, value: str) -> str:
        """ Ensure the received reference contains a valid payment_type_id and
        user_id """
        payment_type_id = value.split("__")[0]
        user_id = value.split("__")[2]

        try:
            PaymentTypeModel.objects.get(id=payment_type_id)
        except PaymentTypeModel.DoesNotExist:
            raise serializers.ValidationError("Payment type does not exist")

        UserModel = get_user_model()
        payment_type_id = value.split("__")[0]
        
        try:
            UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return value

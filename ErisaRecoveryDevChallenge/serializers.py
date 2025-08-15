from rest_framework import serializers
from .models import ClaimsModel, ClaimDetailsModel

class ClaimDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimDetailsModel
        fields = ['denial_reason', 'cpt_codes']

class ClaimsModelSerializer(serializers.ModelSerializer):
    claim_details_model = ClaimDetailsModelSerializer(read_only=True)
    class Meta:
        model = ClaimsModel
        fields = ['id', 'patient_name', 'billed_amount', 'paid_amount', 'status', 'insurer_name', 'discharge_date', 'claim_details_model']

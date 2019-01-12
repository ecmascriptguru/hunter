from rest_framework import serializers
from .models import Credential


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ('email', 'password', 'recovery_email', 'recovery_phone', 'proxy', )
        depth = 1
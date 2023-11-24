from rest_framework import serializers
from .models import UserData

class UserDataSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = UserData
        fields = ['id', 'photo', 'current_occupation', 'address', 'loan_amount', 'purpose', 'date_of_application', 'organization_working_under', 'user']

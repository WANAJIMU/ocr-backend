from rest_framework import serializers
from .models import Check, OCRData, UserData

class UserDataSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = UserData
        fields = ['id', 'photo', 'current_occupation', 'address', 'loan_amount', 'purpose', 'date_of_application', 'organization_working_under', 'user']



class CheckSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Check
        fields = ('id', 'image_1')



class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(write_only=True)


class OCRDataSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)  
    
    class Meta:
        model = OCRData
        fields = ('id', 'image', 'text')



from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','password','email','shipping_address','profile_photo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        photo = validated_data.pop('profile_photo', None)
        user = CustomUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            shipping_address=validated_data['shipping_address'],
            
        )
        user.set_password(validated_data['password'])
        if photo:
            user.profile_photo = photo
        user.save()
        return user
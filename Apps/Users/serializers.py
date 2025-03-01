from rest_framework import serializers
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
          model=User
          fields=[
               'username','password'
          ]

    def create(self, validated_data):
        password= validated_data.pop('password')
        instance=self.Meta.model(**validated_data)
        if password is not None:
             instance.set_password(password)
             instance.save()
        return validated_data
     
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


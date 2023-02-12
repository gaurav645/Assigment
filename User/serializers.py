from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

## For User Regestation by username and password
class RegisterSerializer(serializers.Serializer):
   username=serializers.CharField()
   password=serializers.CharField()

   def validate(self, data):
      if User.objects.filter(username=data['username']).exists():
         raise serializers.ValidationError('username is already taken')
      
      return data

   def create(self, validated_data):
      user=User.objects.create(username=validated_data['username'].lower())
      user.set_password(validated_data['password'])
      user.save()

      return validated_data


## For Login by username and password
class LoginSerializer(serializers.Serializer):
   username=serializers.CharField()
   password=serializers.CharField()

   def validate(self, data):

      if not User.objects.filter(username=data['username']).exists():
         raise serializers.ValidationError('Account not found')
      
      return data

   def get_jwt_token(self, data):
      user=authenticate(username=data['username'], password=data['password'])

      if not user:
         return{'message':'invalid credentials', 'data' : {}}

      refresh = RefreshToken.for_user(user)

      return{'message':'login success', 'data': {'token':{
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }}}
            
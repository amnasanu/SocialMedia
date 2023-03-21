from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post, Tag, Like,Image


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    is_admin = serializers.BooleanField(default=False)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data['is_admin'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Invalid username/password.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        return data
    

# adding post from admin users    
class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField()

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    created_date = serializers.DateTimeField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(post=post, image=image_data)
        return post

  
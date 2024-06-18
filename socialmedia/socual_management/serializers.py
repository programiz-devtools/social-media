from rest_framework import serializers
from .models import User,Post,ImageUpload
from django.contrib.auth import authenticate

class SignupSerializer(serializers.Serializer):
  

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
  

    def validate(self, data):
      
        password = data['password']
        confirm_password = data['confirm_password']
        username = data['username']
        email = data['email']
       

        if email == None:
            raise serializers.ValidationError("Email is required")

        if password != confirm_password:
            raise serializers.ValidationError('Password does not match')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already in use')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already in use')

        return data

    def create(self, validated_data):
     
     validated_data.pop('confirm_password')
     user = User.objects.create(
         username=validated_data['username'],
         email=validated_data['email'],
        
    )
     user.set_password(validated_data['password'])
     user.save()
     


    
     return user
    

class LoginSerializer(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField(write_only=True)

        def validate(self, data):
        
            email = data.get('email')
            password = data.get('password')

            if email and password:
                user = authenticate(email=email, password=password)

                if user:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Unable to log in with the provided credentials.')
            else:
                raise serializers.ValidationError('Must include username" and password')

            return data


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    liked_by = UserSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_date', 'author', 'liked_by']

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'title', 'image']
        
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer,LoginSerializer,PostCreateSerializer,PostSerializer,ImageUploadSerializer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework import serializers
from .models import User,Post
from rest_framework import generics
from django.conf import settings
from django.contrib.auth import authenticate
import os
from .permission import IsJWTAuthenticated
from rest_framework.permissions import IsAuthenticated

def handle_validation_error(e):
   
    response={}
   
    try:
        error_message = str(e).split("ErrorDetail(string='")[1].split("'")[0]

        return Response(
                {"message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
     
           
    except Exception as e:
        return Response(
            
           {"message":"Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
 
        )

class SignUpView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes=[]
    authentication_classes=[]

    def create(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        import pdb;pdb.set_trace()

        try:
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            profile_image=request.FILES.get("profile_image")
            _,file_extension=os.path.splitext(profile_image.name)
            file_name=f"{user.id}{file_extension}"
            image_folder=os.path.join(settings.MEDIA_ROOT,'profiles')

            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            _,file_extension=os.path.splitext(profile_image.name)
                
            file_name=f"{user.id}{file_extension}"
            file_path=os.path.join(image_folder,file_name)
           
            if user.profile_image and os.path.exists(file_path):
                os.remove(file_path)
          
       
            with open(file_path,'wb+') as destination:
                for chunk in profile_image.chunks():
                    destination.write(chunk)

            user.profile_image=f"{file_name}"
            user.save()

            print(serializer.validated_data)
            user1 = User.objects.get(username=serializer.data['username'])
            return Response(serializer.data,status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        
class LoginView(generics.CreateAPIView):
    permission_classes=[]
    authentication_classes=[]
    serializer_class = LoginSerializer
    authentication_classes=[]
    permission_classes=[]

    def create(self, request, *args, **kwargs):
      
      
        serializer =  self.get_serializer(data=request.data)
        try:

       
            serializer.is_valid(raise_exception = True)
            user = serializer.validated_data["user"]
            username=user.username
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
          
            user = authenticate(email=email, password=password)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access["user_type"]=user.user_type
            access_token=str(access)

            return Response({"access_token":access_token})
        
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        

class PostCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsJWTAuthenticated]
   
   
    
    def post(self, request, *args, **kwargs):
        # Extract data from request
        title = request.data.get('title')
        content = request.data.get('content')


        # Create Post object using ORM directly
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        post_serializer = PostCreateSerializer(post)


        return Response({'message': 'Post created successfully'
        }, status=status.HTTP_201_CREATED)
    

class PostLikeAPIView(APIView):
    permission_classes = [IsJWTAuthenticated]
    authentication_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.liked_by.filter(id=user.id).exists():
            return Response({'message': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.liked_by.add(user)
        return Response({'message': 'Like added successfully', 'post_id': post.id}, status=status.HTTP_201_CREATED)
    
class PostUnlikeAPIView(APIView):
    permission_classes = [IsJWTAuthenticated]
    authentication_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if not post.liked_by.filter(id=user.id).exists():
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.liked_by.remove(user)
        return Response({'message': 'Like removed successfully', 'post_id': post.id}, status=status.HTTP_200_OK)
    

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ImageUploadView(APIView):
   

    def post(self, request, *args, **kwargs):
     
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


           

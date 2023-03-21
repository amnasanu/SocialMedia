from rest_framework import viewsets , status
from .serializer import RegisterUserSerializer, UserLoginSerializer, PostSerializer
from rest_framework.response import Response
from django.contrib.auth import login
from .models import Post



class RegisterUserViewSet(viewsets.ViewSet):
    serializer_class = RegisterUserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id})
        return Response(serializer.errors, status=400)
    


class UserLoginViewSet(viewsets.ViewSet):
    serializer_class = UserLoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({'detail': 'Logged in successfully.'}, status=status.HTTP_200_OK)
    
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
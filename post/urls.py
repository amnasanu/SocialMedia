from django.urls import path,include
from rest_framework import routers
from .views import RegisterUserViewSet, UserLoginViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns=[
     path('register/', RegisterUserViewSet.as_view({'post': 'create'}), name='register-user'),
     path('login',UserLoginViewSet.as_view({'post':'create'}),name='user-login'),
     path('', include(router.urls)),

]
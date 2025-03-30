from django.urls import path, include
from .views import RegisterView, LoginView, FollowUserView, UnfollowUserView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
    path('users/<int:pk>/follow/', UserViewSet.as_view({'post': 'follow'}), name='follow-user'),
    path('users/<int:pk>/unfollow/', UserViewSet.as_view({'post': 'unfollow'}), name='unfollow-user'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]

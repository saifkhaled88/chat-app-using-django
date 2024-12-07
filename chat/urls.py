from .views import MessageListView,MessageCreateView,MessageUpdateView,MessageDeleteView,LoginView,RegisterView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.permissions import AllowAny

urlpatterns = [

    # Authentication endpoints
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('login/',LoginView.as_view(), name="login"),
    path('register/',RegisterView.as_view(), name="register"),
    path('message/', MessageListView.as_view(), name="message"),
    path('create-message/', MessageCreateView.as_view(), name="create-message"),
    path('update-message/<str:pk>', MessageUpdateView.as_view(), name="update-message"),
    path('delete-message/<str:pk>', MessageDeleteView.as_view(), name="delete-message"),
]
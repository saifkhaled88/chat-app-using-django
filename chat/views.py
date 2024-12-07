from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage,CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from.serializers import ChatMessageModelSerializer, LoginSerializer, RegisterSerializer


class LoginView(APIView):

    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.create(serializer.validated_data)
            return Response(tokens,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    
    permission_classes = [AllowAny]

    def post(self,request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "user created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MessageListView(generics.ListAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageModelSerializer
    permission_classes = [IsAuthenticated]
    


class MessageCreateView(generics.CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageModelSerializer
    permission_classes = [IsAuthenticated]


class MessageUpdateView(generics.UpdateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageModelSerializer
    permission_classes = [IsAuthenticated]


class MessageDeleteView(generics.DestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageModelSerializer
    permission_classes = [IsAuthenticated]

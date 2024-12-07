from rest_framework import serializers
from .models import ChatMessage,CustomUser
from django.contrib.auth import get_user_model,authenticate
from rest_framework_simplejwt.tokens import RefreshToken

#User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        user = authenticate(username = data['username'], password = data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user' : user}
    
    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
        }




class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2','first_name', 'last_name', 'phone_number' , 'date_of_birth' ]

    def validate(self, data):
        print("Validating data:", data)


        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match!")
        return data
    
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 field

        username = validated_data.get('username')
        if not username:
            raise serializers.ValidationError("Username is required.")

        return CustomUser.objects.create_user(
            username=username,
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            date_of_birth=validated_data.get('date_of_birth')
        )
        




class ChatMessageModelSerializer(serializers.ModelSerializer):

    sender = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )
    receiver = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )


    class Meta:
        model = ChatMessage
        fields = ['sender', 'receiver', 'content', 'timestamp']


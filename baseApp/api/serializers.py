from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError  # Import ValidationError
from rest_framework import serializers
from ..models import CustomUser
#we need this to retrive the user model from db
from django.contrib.auth import get_user_model

User = get_user_model()

class MyTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(f"User : {user}" )
        token = super().get_token(user)

        # Add custom claims
        #token['username'] = user.username
        token['email'] = user.email

        return token
    
    @classmethod
    def validate(cls, attrs):
        # Instead of username, validate with email
        email = attrs.get('email')
        password = attrs.get('password')
        print(f"Email {email}")
        
                # Debugging: Print the email
        print(f"Trying to authenticate with email: {email}")
        
        user = CustomUser.objects.filter(email=email).first()
        data={}
        # Debugging: Print user object
        print(f"Found user: {user}")
        
        #user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise ValidationError('Invalid email or password')
                # Call the superclass method to generate tokens
        #data = super().validate(attrs)
        # Serialize the user object
        print(f"--------------{user}")
        serialized_user = CustomUserSerializer(user)
        data['user']=serialized_user
        # # Explicitly call get_token
        token = cls.get_token(user)
        #  # Add the token data to the response
        # data['access'] = str(token.access_token)  # Add access token
        # data['refresh'] = str(token)               # Add refresh token
        # print(f"This is data {data}")
        return {'user': serialized_user.data, 'token':{'access':str(token.access_token), 'refresh':str(token)}}

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'is_staff', 'is_active','is_superuser','date_joined']  # Add other fields as necessary
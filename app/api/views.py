from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User


@api_view(['POST', 'GET'])
def subscribe_view(request):
    try:
        if request.method == 'POST':
            user_full_name = request.data.get('full_name')
            user_email = request.data.get('email')

            if not user_email:
                return Response({'error': 'Email is required'}, status=400)
            
            try:
                validate_email(user_email)
            except ValidationError:
                return Response({'error': 'Enter valid email'}, status=400)
            
            if User.objects.filter(user_email=user_email).exists():
                return Response({'error': 'User already exists'})
            
            full_name = user_full_name.split(" ")
            
            first_name = full_name[0]
            last_name = ' '.join(full_name[1:])

            user = User(first_name=first_name, last_name=last_name, user_email=user_email)
            user.save()
            user_serializer = UserSerializer(user)

            return Response({"message": "subscribed successfully", "user": user_serializer.data}, status=201)
        
        if request.method == 'GET':
            subscribed_users = User.objects.all()
            subscribed_users_serializer = UserSerializer(subscribed_users, many=True)
            return Response(subscribed_users_serializer.data)

        
    except Exception as e:
        raise APIException('Server error: {}'.format(str(e)))


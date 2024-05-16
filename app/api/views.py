from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import SubscriberSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Subscriber


@api_view(['POST', 'GET'])
def subscribe_view(request):
    try:
        if request.method == 'POST':
            subsciber_full_name = request.data.get('full_name')
            subscriber_email = request.data.get('email')

            if not subscriber_email:
                return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                validate_email(subscriber_email)
            except ValidationError:
                return Response({'error': 'Enter valid email'}, status=status.HTTP_400_BAD_REQUEST)
            
            if Subscriber.objects.filter(user_email=subscriber_email).exists():
                return Response({'error': 'User already exists'})
            
            full_name = subsciber_full_name.split(" ")
            
            first_name = full_name[0]
            last_name = ' '.join(full_name[1:])

            subscriber = Subscriber(first_name=first_name, last_name=last_name, user_email=subscriber_email)
            subscriber.save()
            subscriber_serializer = SubscriberSerializer(subscriber)

            return Response({"message": "subscribed successfully", "user": subscriber_serializer.data}, status=status.HTTP_201_CREATED)
        
        if request.method == 'GET':
            subscribed_users = Subscriber.objects.all()
            subscribed_users_serializer = SubscriberSerializer(subscribed_users, many=True)
            return Response(subscribed_users_serializer.data)

        
    except Exception as e:
        raise APIException({'error': 'Server error', 'details': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


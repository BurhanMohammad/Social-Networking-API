
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django_ratelimit.decorators import ratelimit

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    if email and password:
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # Create user
        user = User.objects.create_user(email=email, password=password,first_name=first_name,last_name=last_name )
        if user:
            # Automatically log in the user after signup
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid signup data'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email and password:
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        
from rest_framework.pagination import PageNumberPagination
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('q', '').lower()
    if '@' in query:
        users = User.objects.filter(email__iexact=query)
    else:
        users = User.objects.filter(Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)



from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='3/m', method='POST', block=True)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get('to_user_id')
    to_user = User.objects.get(id=to_user_id)
    print(to_user, "eee")
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user, status='pending')
    return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_friend_request(request, request_id):
    action = request.data.get('action')
    print("Request ID:", request_id)
    print("Action:", action)
    
    try:
        # Retrieve the FriendRequest object based on request_id
        friend_request = FriendRequest.objects.get(id=request_id)
        print("Friend Request Found ID:", friend_request.id)
        
        # Ensure that the authenticated user is the recipient of the friend request
        if friend_request.to_user != request.user:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        # Perform action based on the provided action parameter
        if action == 'accept':
            friend_request.status = 'accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the updated status
        friend_request.save()
        
        return Response({'message': f'Friend request {action}ed'}, status=status.HTTP_200_OK)
    
    except FriendRequest.DoesNotExist:
        print("Friend Request Not Found")
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        print("Friend Request Not Found")
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = User.objects.filter(Q(sent_requests__to_user=request.user, sent_requests__status='accepted') | Q(received_requests__from_user=request.user, received_requests__status='accepted'))
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
     # Get user IDs for pending friend requests sent to the authenticated user
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending').values_list('from_user_id', flat=True)
    
    # Get user IDs for pending friend requests sent from the authenticated user
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending').values_list('to_user_id', flat=True)
    
    # Combine user IDs from both sent and received requests
    all_pending_users_ids = set(received_requests) | set(sent_requests)
    
    # Get users associated with pending requests
    all_pending_users = User.objects.filter(id__in=all_pending_users_ids)
    
    # Debug print to check the pending users
    print("All Pending Users:", all_pending_users)
    
    serializer = UserSerializer(all_pending_users, many=True)
    return Response(serializer.data)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .pagination import UserPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response({'error': 'Keyword is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search by exact email
        if '@' in keyword:
            users = CustomUser.objects.filter(email__iexact=keyword)
        else:
            # Search by partial name
            users = CustomUser.objects.filter(email__icontains=keyword)
        
        paginator = UserPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = CustomUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver_email = request.data.get('receiver_email')
        receiver = get_object_or_404(CustomUser, email=receiver_email)
        # Check if the sender has sent more than 3 friend requests in the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(sender=sender, created_at__gte=one_minute_ago)
        
        if recent_requests.count() >= 3:
            return Response({'error': 'Cannot send more than 3 friend requests per minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status=FriendRequest.STATUS_PENDING).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        request_id = request.data.get('request_id')
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=user, status=FriendRequest.STATUS_PENDING)
        friend_request.status = FriendRequest.STATUS_ACCEPTED
        friend_request.save()
        return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)

class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        request_id = request.data.get('request_id')
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=user, status=FriendRequest.STATUS_PENDING)
        friend_request.status = FriendRequest.STATUS_REJECTED
        friend_request.save()
        return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)

class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Fetch friends where the current user is either sender or receiver and the request is accepted
        friends_as_sender = FriendRequest.objects.filter(sender=user, status=FriendRequest.STATUS_ACCEPTED).values_list('receiver', flat=True)
        friends_as_receiver = FriendRequest.objects.filter(receiver=user, status=FriendRequest.STATUS_ACCEPTED).values_list('sender', flat=True)

        # Combine friend IDs from both sender and receiver
        friend_ids = set(friends_as_sender) | set(friends_as_receiver)

        # Fetch user objects for these friend IDs
        friends = CustomUser.objects.filter(id__in=friend_ids)
        serializer = CustomUserSerializer(friends, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class ListPendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Fetch pending friend requests where the current user is the receiver
        pending_requests = FriendRequest.objects.filter(receiver=user, status=FriendRequest.STATUS_PENDING)
        serializer = FriendRequestSerializer(pending_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

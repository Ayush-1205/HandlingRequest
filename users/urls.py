from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('send_friend_request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list_friends/', ListFriendsView.as_view(), name='list_friends'),
    path('list_pending_friend_requests/', ListPendingFriendRequestsView.as_view(), name='list_pending_friend_requests'),

]

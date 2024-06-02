
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('search_users/', views.search_users, name='search_users'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('respond_friend_request/<int:request_id>/', views.respond_friend_request, name='respond_friend_request'),
    path('list_friends/', views.list_friends, name='list_friends'),
    path('list_pending_requests/', views.list_pending_requests, name='list_pending_requests'),
]

"""studymate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import user.views as user_views
import topic.views as topic_views
import collaborate.views as collaborate_views
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # test api is working
    path('api/test/', user_views.hello),
    # login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # user
    path('api/users/register/', user_views.CreateUserView.as_view(), name='user_register'),
    path('api/change_password/<int:pk>/', user_views.ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('api/update_profile/<int:pk>/', user_views.UpdateProfileView.as_view(),
         name='auth_update_profile'),
    path('api/user/topics/', collaborate_views.profile.as_view(), name='user-profile'),
    # topics
    path('api/topics/children/<int:id>', topic_views.TopicChildrenView.as_view(), name='get_topic_children'),
    path('api/topics/roots', topic_views.TopicRootsView.as_view(), name='get_topic_children'),
    path('api/topics/tree/<int:id>', topic_views.TopicSubtreeView.as_view(), name='get-topic-subtree'),
    path('api/topics/tree', topic_views.TopicTreeView.as_view(), name='get-topic-tree'),
    # demands (inactive group)
    path('api/demands/create', collaborate_views.CreateGroupView.as_view(), name='create-demand'),
    path('api/demands/all', collaborate_views.AllDemandsView.as_view(), name='all-demands'),
    path('api/demands/owned', collaborate_views.OwnedDemandsView.as_view(), name='owned-demands'),
    path('api/demands/search', collaborate_views.SearchDemandsView.as_view(), name='search-demands'),
    path('api/delete/<int:pk>', collaborate_views.DeleteOwnedDeactiveGroupsView.as_view(), name='delete-demands'),
    # active groups
    path('api/groups/all', collaborate_views.AllActiveGroupsView.as_view(), name='all-active-groups'),
    path('api/groups/owned/', collaborate_views.OwnedActiveGroupsView.as_view(), name='owned-active-groups'),
    path('api/groups/joined', collaborate_views.JoinedGroupsView.as_view(), name='my-joined-groups'),
    path('api/groups/members/<int:pk>', collaborate_views.GroupMembers.as_view(), name='group-members'),
    # join requests
    path('api/join', collaborate_views.MakeJoinRequest.as_view(), name='make-join-request'),
    path('api/requests/sent', collaborate_views.SentJoinRequests.as_view(), name='sent-join-requests'),
    path('api/requests/owned', collaborate_views.OwnedGroupsJoinRequests.as_view(), name='owned-group-join-requests'),
    path('api/requests/answer/<int:pk>', collaborate_views.AnswerJoinRequest.as_view(),
         name='answer-join-request'),
    # chat urls    
    path('chat/<int:pk>/', collaborate_views.message_group.as_view(), name='group-chats'),
    path('chat/update/<int:pk>/', collaborate_views.messege_update.as_view(),
         name='group-chats'),
#     path('chat/<int:receiver>/',
#          collaborate_views.message_user_show.as_view(), name='user-group-chat'),
    path('api/messages/', collaborate_views.message_create.as_view(),
         name='message-create'),
    # rating urls
    path('api/rating_members/<int:pk>/', collaborate_views.GP_rate_members.as_view(),
         name='partner-view'),
    path('api/rating/<int:pk>/', collaborate_views.GPrating_create.as_view(),
         name='partner-rating'),
    path('api/pending_delete/<int:group_id>/',
         collaborate_views.DeletePendingGroupsView.as_view(), name='delete-group'),
    
    # dashboard
    path('api/dashboard/', collaborate_views.dashboard.as_view(), name='personal-dashboard'),
    # documentation
#     path('docs/', include_docs_urls(title='Study mate API documentation', public=True))
]

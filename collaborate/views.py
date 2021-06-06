from collaborate.serializers import GroupSerializer, GroupSearchSerializer, JoinRequestSerializer, \
    AnswerJoinRequestSerializer, MessengerSerializer, dashboardSerializer, GP_rateSerializer, Avg_RateSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from collaborate.models import Group, JoinRequest, Messenger, GP_Rate
from rest_framework.views import APIView
from django.db.models import Func, F
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from user.serializers import SimpleUserSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, get_user_model


class CreateGroupView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        active=False,is_pending=False)


class OwnedActiveGroupsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer    

    def get_queryset(self):
        return Group.objects.filter(owner=self.request.user, active=True).order_by('-created_at')

class OwnedDeactiveGroupsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(owner=self.request.user, active=False).order_by('-created_at')

class OwnedDemandsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(owner=self.request.user, active=False).order_by('-created_at')

class DeleteOwnedDeactiveGroupsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllActiveGroupsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.filter(active=True).order_by('-created_at')    


class AllDemandsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.filter(active=False).order_by('-created_at')


class JoinedGroupsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def get_queryset(self):
        return self.request.user.joined_groups


class SearchDemandsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = GroupSearchSerializer(data=request.data)
        serializer_class = Avg_RateSerializer(user = request.user)
        if serializer.is_valid():
            # just searching in inactive groups (demands)
            topic = serializer.validated_data.get('topic')
            weeks = serializer.validated_data.get('weeks')
            avgRate = serializer_class.validated_data.get('avgRate')
            hours = serializer.validated_data.get('hours_per_week')
            groups = Group.objects.filter(active=False, topic=topic).annotate(
                weeks_diff=Func(F('weeks') - weeks, function='ABS'),
                hours_diff=Func(F('hours_per_week') - hours, function='ABS')
            ).order_by('hours_diff', 'weeks_diff')
            # TODO: paginate later
            group_serializer = GroupSerializer(groups, many=True)
            return Response(group_serializer.data, status=200)
        else:
            return Response(serializer.errors)


class MakeJoinRequest(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OwnedGroupsJoinRequests(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinRequestSerializer

    def get_queryset(self):
        return JoinRequest.objects.filter(group__owner=self.request.user)


class SentJoinRequests(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinRequestSerializer

    def get_queryset(self):
        return JoinRequest.objects.filter(user=self.request.user)


class AnswerJoinRequest(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerJoinRequestSerializer

    def get_queryset(self):
        return JoinRequest.objects.filter(group__owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if instance.accepted is not None:
            raise ValidationError({"detail": "request is already answered"}, code=status.HTTP_403_FORBIDDEN)
        if serializer.validated_data.get('accepted'):
            group = instance.group
            if not group.active:
                group.active = True
                group.members.add(group.owner)
            group.members.add(instance.user)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GroupMembers(ListAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        pk = int(self.kwargs.get(self.lookup_url_kwarg))
        group = get_object_or_404(Group, pk=pk)
        return group.members


class message_user_show(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = MessengerSerializer

    @csrf_exempt
    def message_show(self, request, sender=None, receiver=None):
       
        messages = Messenger.objects.filter(
            sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessengerSerializer(
        messages, many=True, context={'request': request})
        

        return Response(serializer.data, safe=False)      


class message_group(ListAPIView):

    permission_classes=(IsAuthenticated,)
    serializer_class=MessengerSerializer
    
    def get_queryset(self):
        return Messenger.objects.filter(receiver__owner = self.request.user.id)

    @ csrf_exempt
    def update(self, request, receiver=None):
        if receiver.is_pending == True:
            redirect('partner-rating')
        else:    
            messages=Messenger.objects.filter(receiver_id = receiver)
            serializer=MessengerSerializer(
            messages, many=True, context={'request': request})
            for message in messages:
                if message.sender != request.user:
                    message.is_read = True
                    message.save()
            return Response(serializer.data, safe=False)


class dashboard(ListAPIView):
    
    serializer_class = dashboardSerializer
    premission_classes = (IsAuthenticated,)

    def get(self, request, owner=None):
        groups = Group.objects.filter(
            active=True, owner=owner).order_by('created_at')
        serializer = dashboardSerializer(groups, context={'request': request})
        return Response(serializer.data)

class profile(ListAPIView):
    premission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        return get_user_model().objects.all(), OwnedDeactiveGroupsView()


class message_create(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessengerSerializer

    @csrf_exempt
    def message_create(self, request, sender=None, receiver=None):
        data = JSONParser().parse(request)
        serializer = MessengerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

        
class GPrating_create(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GP_rateSerializer
    serializer = Avg_RateSerializer

    def get_users(self, request, rating_user=None, group_id=None):
        group = Group.objects.filter(id=group_id)
        
        if rating_user == group.owner:
            return Group.members.filter(id=group.id)
        else:
            return Group.members.filter(id=group.id), GP_Rate.duration.filter(group=group)
        
    

    def GPrating_create(self, request, rating_user=None, group_id=None):
        group = Group.objects.filter(id=group_id)
        data = JSONParser().parse(request)
        serializer = GP_rateSerializer(data=data)
        
        if serializer.isvalid():
            if rating_user == group.owner:
                group.is_pending = True
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                serializer.save()
                redirect()
        return Response(serializer.errors, status = 400)

class Avg_Show(APIView):
    serializer_class = Avg_RateSerializer

    def get_queryset(self):
        return Response(serializer_class.data, status=status.HTTP_200_OK)


# after second user submits
class DeletePendingGroupsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    def delete(self, request, group_id, format=None):
        event = self.get_object(group_id)
        event.delete()
        redirect('personal-dashboard')


from rest_framework import serializers
from collaborate.models import Group, JoinRequest, Messenger#, GP_Rate, Avg_Rate

from user.serializers import SimpleUserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from topic.serializers import TopicSerializer
from topic.models import Topic
from rest_framework import status


class GroupSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(many=False, read_only=True)
    topic = TopicSerializer(many=False, read_only=True)
    specified_topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), write_only=True)

    

    # TODO: topic should be at fourth level

    class Meta:
        model = Group
        fields = (
            'id', 'owner', 'active', 'created_at', 'hours_per_week', 'topic', 'specified_topic', 'weeks', 'slug',
            'description')
        read_only_fields = ('id', 'active', 'created_at')
        write_only_fields = ('specified_topic',)

    def create(self, validated_data):
        topic = validated_data.pop('specified_topic')
        validated_data['topic'] = topic
        return Group.objects.create(**validated_data)

    

    


# TODO: simple group serializer for read

class GroupSearchSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    # TODO: topic should be at fourth level

    class Meta:
        model = Group
        fields = ('topic', 'hours_per_week', 'weeks')


class JoinRequestSerializer(serializers.ModelSerializer):
    specified_group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)

    group = GroupSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    # todo: group and user should be unique together
    class Meta:
        model = JoinRequest
        fields = ('id', 'group', 'specified_group', 'user', 'accepted')
        read_only_fields = ('id', 'group', 'user', 'accepted')
        write_only_fields = ('specified_group',)

    def create(self, validated_data):
        group = validated_data.pop('specified_group')
        validated_data['group'] = group
        if group.owner_id == validated_data['user'].id:
            raise serializers.ValidationError({"detail": "group owner cannot request to join."},
                                              code=status.HTTP_403_FORBIDDEN)
        if group.members.filter(user__id=validated_data['user'].id).exists():
            raise serializers.ValidationError({"detail": "group members cannot request to join"},
                                              code=status.HTTP_403_FORBIDDEN)
        return JoinRequest.objects.create(**validated_data)


class AnswerJoinRequestSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)
    accepted = serializers.BooleanField(allow_null=False)
    lookup_url_kwarg = 'request_id'

    class Meta:
        model = JoinRequest
        fields = ('id', 'group', 'user', 'accepted')
        read_only_fields = ('group', 'user')


class MessengerSerializer(serializers.ModelSerializer):
    
    sender = SimpleUserSerializer(read_only = True)
    receiver = GroupSerializer(read_only=True)
    text = serializers.CharField()
    sentAt = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Messenger
        fields = ['sender', 'receiver', 'text', 'sentAt']


class dashboardSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(many=False, read_only=True)
    topic = TopicSerializer(many=False, read_only=True)
    
    newMesseges = serializers.SerializerMethodField()


    class Meta:
        model = Group
        fields=['topic', 'owner', 'newMesseges']

    def get_newMesseges(self, obj):
        messeges = Messenger.objects.all()
        request = self.context.get('request')
        count = 0
        for messege in messeges:
            if messege.receiver == obj and messege.is_read == False and messege.sender.id != request.user.id:
                count = count + 1
        return count
        


# class GP_rateSerializer(serializers.ModelSerializer):
#     user = SimpleUserSerializer(read_only=True)
#     group = GroupSerializer(read_only = True)
#     rate = serializers.SmallIntegerField()
#     duration = serializers.SmallIntegerField()
    
#     class Meta:
#         model = GP_Rate
#         fields = ['user', 'group', 'rate', 'duration']


# class Avg_RateSerializer(serializers.ModelSerializer):
#     user = SimpleUserSerializer(read_only=True)
#     overal_duration = serializers.IntegerField()
#     class Meta:
#         model = Avg_Rate
#         fields = ['user', 'overal_duration']

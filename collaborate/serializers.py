from rest_framework import serializers
from collaborate.models import Group, JoinRequest, Messenger, GP_Rate

from user.serializers import SimpleUserSerializer, userAndRateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from topic.serializers import TopicSerializer
from topic.models import Topic
from rest_framework import status


class GroupSerializer(serializers.ModelSerializer):
    owner = userAndRateSerializer(many=False, read_only=True)
    topic = TopicSerializer(many=False, read_only=True)
    specified_topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), write_only=True)

    

    # TODO: topic should be at fourth level

    class Meta:
        model = Group
        fields = (
            'id', 'owner', 'active', 'created_at', 'hours_per_week', 'topic', 'specified_topic', 'weeks', 'slug',
            'description', 'is_pending')
        read_only_fields = ('id', 'active', 'created_at','is_pending')
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
    #    if group.owner_id == validated_data['user'].id:
#             raise serializers.ValidationError({"detail": "group owner cannot request to join."},
#                                               code=status.HTTP_403_FORBIDDEN)
#         if group.members.filter(user__id=validated_data['user'].id).exists():
#             raise serializers.ValidationError({"detail": "group members cannot request to join"},
#                                               code=status.HTTP_403_FORBIDDEN)
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
    
    sender = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(
        many=False, slug_field='id', queryset=Group.objects.all())
    text = serializers.CharField()
    sentAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Messenger
        fields = ['sender', 'receiver', 'text', 'sentAt']


class dashboardSerializer(GroupSerializer):
    # owner = serializers.SlugRelatedField(
    #     many=False, slug_field='username', queryset=User.objects.all())
    # topic = serializers.SlugRelatedField(
    #     many=False, slug_field='name', queryset=Group.objects.all())
    newMesseges = serializers.SerializerMethodField()

    # class Meta:
    #     model = Group
    #     fields = ['owner', 'topic', 'newMesseges']
    def get_newMesseges(self, obj):
        messeges = Messenger.objects.all()
        request = self.context.get('request')
        
        count = 0
        for messege in messeges:
            if messege.receiver == obj and messege.is_read == False and messege.sender.id != request.user.id:
                count = count + 1
        obj.newMesseges = count
        return obj.newMesseges       
    
    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + ('newMesseges',)

    



class GP_rateSerializer(serializers.ModelSerializer):
    rating_user = SimpleUserSerializer(read_only=True)
    rated_user = SimpleUserSerializer(read_only=True)
    group = GroupSerializer(read_only = True)
    rate = serializers.IntegerField()
    duration = serializers.IntegerField()
    
    class Meta:
        model = GP_Rate
        fields = ['rating_user','rated_user', 'group', 'rate', 'duration']


# class Avg_RateSerializer(serializers.ModelSerializer):
#     user = SimpleUserSerializer(read_only=True)
#     avgRate = serializers.Field()



#     class Meta:
#         model = Avg_Rate
#         fields = ['user', 'avgRate']

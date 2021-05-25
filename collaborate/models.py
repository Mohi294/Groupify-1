from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from mptt.models import TreeForeignKey
from topic.models import Topic
# from django.core.exceptions import ValidationError



class Group(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, null=False, blank=False,
                              related_name='owned_groups')
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    hours_per_week = models.PositiveSmallIntegerField(null=False)
    topic = TreeForeignKey(Topic, on_delete=models.RESTRICT, null=False)
    weeks = models.PositiveSmallIntegerField(null=False)
    slug = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=True)

    members = models.ManyToManyField(get_user_model(), related_name='joined_groups', blank=True)


class JoinRequest(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests', null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='join_requests')
    accepted = models.BooleanField(null=True, default=None)

    class Meta:
        unique_together = (('group', 'user'),)


class Messenger(models.Model):

    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='reciever', null=False)
    text = models.CharField(max_length=1200)
    sentAt = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('sentAt',)


class GP_Rate(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='retaed_user')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='participated_group')
    rate = models.SmallIntegerField(max_value=10, min_value=0)
    duration = models.SmallIntegerField(max_value=53, min_value=1)

    def __str__(self):
        return self.rate

    class Meta:
        ordering = ('user',)

class Avg_Rate(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    avgRate = models.FloatField(min_value = 0, max_value = 10)
    
    def __str__(self):
        return self.avgRate

    class Meta:
        ordering = ('user',)

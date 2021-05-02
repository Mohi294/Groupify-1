from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from topic.serializers import TopicSerializer, TopicSubtreeSerializer
from topic.models import Topic
from django.shortcuts import get_object_or_404


class TopicChildrenView(ListAPIView):
    """
    returns topic children
    """
    serializer_class = TopicSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        pk = int(self.kwargs.get(self.lookup_url_kwarg))
        topic = get_object_or_404(Topic, id=pk)
        return topic.get_children()


class TopicRootsView(ListAPIView):
    """
    returns root topics
    """
    serializer_class = TopicSerializer
    queryset = Topic.objects.filter(level=0)


class TopicSubtreeView(RetrieveAPIView):
    """
    returns subtree from given node
    """
    serializer_class = TopicSubtreeSerializer
    lookup_url_kwarg = 'id'

    def get_object(self):
        pk = int(self.kwargs.get(self.lookup_url_kwarg))
        topic = get_object_or_404(Topic, id=pk)
        return topic


class TopicTreeView(ListAPIView):
    """
    returns the whole tree
    """
    serializer_class = TopicSubtreeSerializer
    queryset = Topic.objects.filter(level=0)

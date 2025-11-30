from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Topic, FeedItem
from subscriptions.models import Subscription
from .serializers import TopicSerializer, FeedItemSerializer, SubscriptionSerializer
from users.models import CustomUser

class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class MySubscriptionsView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)

class SubscribeView(APIView):
    def post(self, request):
        user = request.user
        topic_id = request.data.get('topic_id')

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        subscription, created = Subscription.objects.get_or_create(user=user, topic=topic)

        if created:
            return Response({'message': 'Subscribed to topic'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already subscribed to topic'}, status=status.HTTP_200_OK)

class UnsubscribeView(APIView):
    def post(self, request):
        user = request.user
        topic_id = request.data.get('topic_id')

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        deleted = Subscription.objects.filter(user=user, topic=topic).delete()
        if deleted[0]:
            return Response({'success': f'Unsubscribed from {topic.name}'})
        return Response({'info': 'Not subscribed'})

class FeedListView(generics.ListAPIView):
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return FeedItem.objects.filter(topic_id=topic_id).order_by('-created_at')
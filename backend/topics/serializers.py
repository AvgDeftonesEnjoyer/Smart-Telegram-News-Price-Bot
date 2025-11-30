from rest_framework import serializers

from .models import Topic, FeedItem
from subscriptions.models import Subscription
from users.models import CustomUser

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = ['id', 'topic', 'title', 'url', 'source', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'topic', 'created_at']
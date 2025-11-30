from django.urls import path
from .views import TopicListView, MySubscriptionsView, SubscribeView, UnsubscribeView, FeedListView

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('subscriptions/', MySubscriptionsView.as_view(), name='my-subscriptions'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('topics/<int:topic_id>/feed/', FeedListView.as_view(), name='feed-list'),
]
from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FeedItem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='feed_items')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)  # Optional detailed content
    url = models.URLField()
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title


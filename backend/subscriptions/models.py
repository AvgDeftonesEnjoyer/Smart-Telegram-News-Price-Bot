from django.db import models
from users.models import CustomUser

class Subscription(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    topic = models.ForeignKey('topics.Topic', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f'{self.user} → {self.topic}'


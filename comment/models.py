from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    article = models.ForeignKey('main.Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Комментарий от {self.author.username}'
    
    @property
    def children(self):
        return self.replies.filter(is_active=True)
    
    @property
    def is_parent(self):
        return self.parent is None
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models


class User(BaseUser):
    objects = BaseUserManager()



class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    
    class Meta:
        unique_together = ('from_user', 'to_user', 'status')
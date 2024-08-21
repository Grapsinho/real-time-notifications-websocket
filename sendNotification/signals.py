from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Comment, Notification

@receiver(post_save, sender=Comment)
def notify_user_on_comment(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            message=f"<span style='font-weight: bold'>{instance.user}</span> commented on your post",
            post=instance.post
        )
        
        # Send notification to WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.post.author.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'message': notification.message,
                    'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'post_id': instance.post.id
                }
            }
        )
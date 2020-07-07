from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from submissions.models import Submission


@receiver(post_save, sender=Submission)
def send_notification(sender, **kwargs):
    print("Database changed, send socket to client")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "submissions-client",
        {
            "type": "database.change",
            "text": "NEW_SUBMISSION_CHANGE",
        },
    )

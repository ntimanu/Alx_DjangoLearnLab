from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification

class NotificationListView(generics.ListAPIView):
    """Retrieve notifications for the authenticated user"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-timestamp')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        notifications = [
            {
                "id": notif.id,
                "actor": notif.actor.username,
                "verb": notif.verb,
                "timestamp": notif.timestamp,
                "read": notif.read
            } for notif in queryset
        ]
        return Response(notifications)

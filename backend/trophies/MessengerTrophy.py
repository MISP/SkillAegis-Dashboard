#!/usr/bin/env python3
from backend.notification import get_notifications
from backend.trophies.AbstractTrophy import Trophy

class MessengerTrophy(Trophy):

    id = "messenger"
    name = "Messenger"
    description = "Post a message to the dashboard"
    icon_path = "assets/chatty_gold.png"

    def is_earned(self, user_id: int, tasks_completion: dict) -> bool:
        notifications = get_notifications()
        for notification in notifications:
            if notification.get('user_id') == user_id and notification.get('target_tool') == 'webhook':
                if 'message' in notification and notification['message'].get('text'):
                    return True
        return False

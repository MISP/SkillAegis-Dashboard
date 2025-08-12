#!/usr/bin/env python3
from backend.notification import get_notifications
from backend.trophies.AbstractTrophy import Trophy

class SpammerTrophy(Trophy):

    id = "spammer"
    name = "Spammer"
    description = "Contribute over 50% of total activity in the live feed"
    icon_path = "assets/bell-notifications.png"

    def is_earned(self, user_id: int, tasks_completion: dict) -> bool:
        notifications = get_notifications()
        if len(notifications) < 30:
            return False

        user_notification_count = len([1 for notif in notifications if notif['user_id'] == user_id])
        return user_notification_count >= (len(notifications) / 2)

#!/usr/bin/env python3
from backend.notification import get_notifications
from backend.trophies.AbstractTrophy import Trophy

class MessengerTrophy(Trophy):

    id = "messenger"
    name = "Messenger"
    description = "Post a message to the dashboard"
    icon_path = "assets/chatty_gold.png"

    def is_earned(self, user_id: int, tasks_completion: dict) -> bool:
        return False
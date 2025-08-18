#!/usr/bin/env python3
from backend.trophies.AbstractTrophy import Trophy

class BounceBackTrophy(Trophy):

    id = "bounce-back"
    name = "Bounce Back"
    description = "Finish an exercise after a 30min break"
    icon_path = "assets/phoenix-noto.png"
    break_in_min = 30

    def is_earned(self, user_id: int, tasks_completion: dict) -> bool:
        timestamps = []
        for inject_uuid, completed in tasks_completion.items():
            if not completed:
                continue
            timestamps.append(completed["timestamp"])
        timestamps.sort()
        timestamp_deltas = [
            timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)
        ]

        return any([delta for delta in timestamp_deltas if delta >= self.break_in_min*60])

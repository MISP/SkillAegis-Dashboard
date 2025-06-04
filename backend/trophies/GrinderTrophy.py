#!/usr/bin/env python3
from backend.trophies.AbstractTrophy import Trophy

class GrinderTrophy(Trophy):

    id = "grinder"
    name = "Grinder"
    description = "Complete every exercise"
    icon_path = "assets/medal_04_gold.png"

    def is_earned(self, user_id: int, tasks_completion: dict) -> bool:
        return len(tasks_completion.keys()) == len(
            [x for x in tasks_completion.values() if x]
        )

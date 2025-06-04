#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any, Dict

import backend.db as db


class Trophy(ABC):

    id = "id"
    name = "name"
    description = "description every exercise"
    icon_path = "icon_path"

    def is_earned_for_users(
        self, selected_exercices: list, completion_for_users: dict
    ) -> list:
        user_that_got_the_trophy = set()
        user_trophies = []
        for user_id in completion_for_users.keys():
            if user_id not in db.USER_ID_TO_EMAIL_MAPPING:
                print("unknown user id", user_id)
                continue
            for exec_uuid, tasks_completion in completion_for_users[user_id].items():
                if exec_uuid in selected_exercices:
                    if self.is_earned(user_id, tasks_completion):
                        if user_id not in user_that_got_the_trophy:
                            user_trophies.append(
                                {
                                    "user_id": user_id,
                                    "email": db.USER_ID_TO_EMAIL_MAPPING[user_id],
                                }
                            )
                            user_that_got_the_trophy.add(user_id)
        return user_trophies

    @abstractmethod
    def is_earned(self, user_id: int, tasks_completion: dict) -> bool:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon_path": self.icon_path,
        }

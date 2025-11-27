import json
from typing import Optional

import redis

r = redis.Redis(host="localhost", port=6379, db=0)


class StepValidateService:
    def __init__(self, user_id: int, flow_name: str, steps: list[str]):
        self.user_id = user_id
        self.flow_name = flow_name
        self.steps = steps
        self.key = f"user:{self.user_id}:{self.flow_name}"
        self._data = self._get_state()

    def _get_state(self):
        raw = r.get(self.key)
        if raw:
            return json.loads(raw)
        return {"current_step": self.steps[0], "data": {}}

    def _save_state(self):
        r.set(self.key, json.dumps(self._data), ex=600)  # expire time 10 minutes

    # Set the current step
    @property
    def current_step(self) -> str:
        """Set current step."""
        return self._data["current_step"]

    def is_step_valid(self, step_name: str) -> bool:
        """Verify that user does't skip step."""

        return self.current_step == step_name

    def advance_step(self, data: Optional[dict] = None):
        """Merge data of current step."""

        if data:
            self._data["data"].update(data)

        # Skip to next step if exists.
        current_index = self.steps.index(self.current_step)
        if current_index + 1 < len(self.steps):
            self._data["current_step"] = self.steps[current_index + 1]
        self._save_state()

    def validate_step(self, step_name: str):
        """
        Validate that the current step is allowed.

        Args:
            step_name (str): The name of the step to validate.

        Raises:
            ValueError: If the step is not allowed.
        """
        if not self.is_step_valid(step_name):
            raise ValueError("Step not allowed.")

    def set_next_step(self, step_name: str):
        """
        Set the next step of change email server.

        Args:
            step_name (str): The name of the next step.
        """

        self.advance_step(data={step_name: True})

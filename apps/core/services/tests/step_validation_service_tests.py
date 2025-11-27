import json
from unittest import TestCase
from unittest.mock import patch

from apps.core.services.step_validate_service import StepValidateService


class StepValidateServiceTestCase(TestCase):

    def setUp(self):
        self.user_id = 1
        self.flow_name = "test_flow"
        self.steps = ["step1", "step2", "step3"]

    @patch("apps.core.services.step_validate_service.r")
    def test_initial_state(self, mock_redis):
        # Simula Redis sem valor salvo
        mock_redis.get.return_value = None

        service = StepValidateService(
            user_id=self.user_id, flow_name=self.flow_name, steps=self.steps
        )
        self.assertEqual(service.current_step, "step1")
        self.assertTrue(service.is_step_valid("step1"))
        self.assertFalse(service.is_step_valid("step2"))

    @patch("apps.core.services.step_validate_service.r")
    def test_advance_step(self, mock_redis):
        mock_redis.get.return_value = None
        service = StepValidateService(
            user_id=self.user_id, flow_name=self.flow_name, steps=self.steps
        )

        # Avança com dados
        service.advance_step(data={"foo": "bar"})
        self.assertEqual(service.current_step, "step2")
        self.assertEqual(service._data["data"]["foo"], "bar")
        mock_redis.set.assert_called()

        # Avança até o último step
        service.advance_step()
        self.assertEqual(service.current_step, "step3")

        # Não deve avançar além do último step
        service.advance_step()
        self.assertEqual(service.current_step, "step3")

    @patch("apps.core.services.step_validate_service.r")
    def test_load_state_from_redis(self, mock_redis):
        # Simula Redis com estado salvo
        saved_data = {"current_step": "step2", "data": {"x": 42}}
        mock_redis.get.return_value = json.dumps(saved_data)

        service = StepValidateService(
            user_id=self.user_id, flow_name=self.flow_name, steps=self.steps
        )
        self.assertEqual(service.current_step, "step2")
        self.assertEqual(service._data["data"]["x"], 42)

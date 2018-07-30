"""Middleware for logging"""

from testbuilder.core.base.basemiddleware import TBBaseMiddleware
from testbuilder.conf import settings

import logging
import sys

class LoggingMiddleware(TBBaseMiddleware):
    def __init__(self):
        self.logger = logging.getLogger()

        log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(log_format)

        self.logger.setLevel(settings["LOG_LEVEL"])

        self.logger.addHandler(console)

    def before_step(self, step_context) -> None:
        action = step_context.step_action
        step_number = step_context.step_number
        status = step_context.step.status

        self.logger.info(f"Action=BeforeStep, Action={action}, Step_Number={step_number}, Status={status}")

    def after_step(self, step_context) -> None:
        action = step_context.step_action
        step_number = step_context.step_number
        status = step_context.step.status

        self.logger.info(f"Action=AfterStep, Action={action}, Step_Number={step_number}, Status={status}")

    def step_failure(self, step_context) -> None:
        action = step_context.step_action
        step_number = step_context.step_number
        status = step_context.step.status
        e = step_context.step_settings["Exception"]

        self.logger.error(f"Action=StepFailure, Action={action}, Step_Number={step_number}, Status={status}, Exception={e}")
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
        argument_1 = step_context.step_argument_1
        step_number = step_context.step_number
        status = step_context.step.status.name

        self.logger.info(f"Log=BeforeStep, Action={action}, Step_Number={step_number}, Status={status}, Arg1={argument_1}")

    def after_step(self, step_context) -> None:
        action = step_context.step_action
        step_number = step_context.step_number
        status = step_context.step.status.name

        self.logger.info(f"Log=AfterStep, Action={action}, Step_Number={step_number}, Status={status}")

    def step_failure(self, step_context) -> None:
        action = step_context.step_action
        step_number = step_context.step_number
        status = step_context.step.status.name
        e = step_context.step_settings["Exception"]

        self.logger.error(f"Log=StepFailure, Action={action}, Step_Number={step_number}, Status={status}, Exception={e}")
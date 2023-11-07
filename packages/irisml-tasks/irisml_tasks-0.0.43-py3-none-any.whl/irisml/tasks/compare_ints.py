import dataclasses
import logging
import irisml.core
from typing import Optional

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """ Compare two int values

    Inputs:
        val1 (int): value 1
        val2 (int): value 2
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        val1: int
        val2: int

    @dataclasses.dataclass
    class Outputs:
        result: bool

    @dataclasses.dataclass
    class Config:
        equal_allowed: Optional[bool] = True
        greater: Optional[bool] = True

    def execute(self, inputs):
        if self.config.equal_allowed and inputs.val1 == inputs.val2:
            return self.Outputs(True)

        return self.Outputs(inputs.val1 > inputs.val2 if self.config.greater else inputs.val1 < inputs.val2)

    def dry_run(self, inputs):
        return self.execute(inputs)

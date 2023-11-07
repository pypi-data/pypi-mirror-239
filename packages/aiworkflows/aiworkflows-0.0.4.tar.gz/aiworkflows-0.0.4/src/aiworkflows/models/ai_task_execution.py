from aiworkflows.models.ai_task_call import AiTaskCall
from aiworkflows.models.ai_task_data_object import AiTaskDataObject
from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field


class AiTaskExecution:
    """
    Represents the execution of an AI task.
    """
    def __init__(self,
                 callstack: list[AiTaskCall],
                 result: AiTaskDataObject = None,
                 success: bool = None,
                 completion_timestamp: int = None,
                 execution_id: str = None,
                 ):
        """
        Initializes a new instance of the AiTaskExecution class.

        :param callstack: The callstack of the task execution.
        :param result: The result of the task execution.
        :param success: Whether the task execution was successful.
        :param completion_timestamp: The timestamp of the task execution.
        :param id: The id of the task execution.
        """
        self.callstack: list[AiTaskCall] = callstack
        self.result: AiTaskDataObject = result
        self.success: bool = success
        self.completion_timestamp: int = completion_timestamp
        self.id: str = execution_id

    @staticmethod
    def from_json(json: dict) -> 'AiTaskExecution':
        """
        Creates a new instance of the AiTaskExecution class from a JSON object.

        :param json: The JSON object.
        """
        callstack = parse_required_field(json, 'callStack', list)
        callstack = [AiTaskCall.from_json(c) for c in callstack]

        result = parse_optional_field(json, 'result', AiTaskDataObject)
        success = parse_optional_field(json, 'success', bool)
        completion_timestamp = parse_optional_field(json, 'completionTimestamp', int)
        execution_id = parse_optional_field(json, 'id', str)

        return AiTaskExecution(callstack=callstack,
                               result=result,
                               success=success,
                               completion_timestamp=completion_timestamp,
                               execution_id=execution_id)

    def to_json(self) -> dict:
        """
        Creates a JSON object from the AiTaskExecution object.
        """
        callstack = [c.to_json() for c in self.callstack]

        return {
            'callStack': callstack,
            'result': self.result,
            'success': self.success,
            'completionTimestamp': self.completion_timestamp,
            'id': self.id
        }

    def __repr__(self):
        return f"AiTaskExecution(callstack={self.callstack}, result={self.result}, success={self.success}, completion_timestamp={self.completion_timestamp})"

    def __str__(self):
        return self.__repr__()

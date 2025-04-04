import warnings
from collections.abc import Callable, Sequence

from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
from agentdojo.functions_runtime import EmptyEnv, Env, FunctionsRuntime
from agentdojo.types import ChatMessage, ChatSystemMessage, ChatUserMessage, ChatToolResultMessage


# class InitQuery(BasePipelineElement):
#     """Initializes the pipeline execution with the user query, by adding a
#     [`ChatUserMessage`][agentdojo.types.ChatUserMessage] to the messages list."""

#     def query(
#         self,
#         query: str,
#         runtime: FunctionsRuntime,
#         env: Env = EmptyEnv(),
#         messages: Sequence[ChatMessage] = [],
#         extra_args: dict = {},
#     ) -> tuple[str, FunctionsRuntime, Env, Sequence[ChatMessage], dict]:
#         if len(messages) > 2 or (len(messages) == 1 and messages[0]["role"] != "system"):
#             warnings.warn("The query is not being added as the first message or after the system message")
#         query_message = ChatUserMessage(role="user", content=query)
#         messages = [*messages, query_message]
#         return query, runtime, env, messages, extra_args
    
class InitQuery(BasePipelineElement):
    """Initializes the pipeline execution with the user query, by adding a
    [`ChatUserMessage`][agentdojo.types.ChatUserMessage] to the messages list."""
    
    def __init__(self, memory_output_formatter: Callable[[str], str] = lambda result: result) -> None:
        self.memory_output_formatter = memory_output_formatter

    def query(
        self,
        query: str,
        runtime: FunctionsRuntime,
        env: Env = EmptyEnv(),
        messages: Sequence[ChatMessage] = [],
        extra_args: dict = {},
    ) -> tuple[str, FunctionsRuntime, Env, Sequence[ChatMessage], dict]:
        if len(messages) > 2 or (len(messages) == 1 and messages[0]["role"] != "system"):
            warnings.warn("The query is not being added as the first message or after the system message")
        query_message = ChatUserMessage(role="user", content=query)
        
        if "memory_injection" in extra_args:
            injection = f"[memory] The following summary of past plans and actions has been retrieved for the user's current task from previous trajectories:\n1."
            injection += extra_args["memory_injection"]
            memory_message = ChatToolResultMessage(role="user", content=self.memory_output_formatter(injection))
            messages = [*messages, query_message, memory_message]
        else:
            messages = [*messages, query_message]
        return query, runtime, env, messages, extra_args


class SystemMessage(BasePipelineElement):
    """Adds a system message to the messages list (as a [`ChatSystemMessage`][agentdojo.types.ChatSystemMessage]).

    Args:
        system_message: the content of the system message.
    """

    def __init__(self, system_message: str) -> None:
        self.system_message = system_message

    def query(
        self,
        query: str,
        runtime: FunctionsRuntime,
        env: Env = EmptyEnv(),
        messages: Sequence[ChatMessage] = [],
        extra_args: dict = {},
    ) -> tuple[str, FunctionsRuntime, Env, Sequence[ChatMessage], dict]:
        if len(messages) > 0:
            raise ValueError("The system message should be the first message")
        system_message = ChatSystemMessage(role="system", content=self.system_message)
        return query, runtime, env, [system_message], extra_args

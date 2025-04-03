from agentdojo.default_suites.v1.chain.injection_tasks import ChainInjectionTask  # noqa: F401 - Register tasks
from agentdojo.default_suites.v1.chain.task_suite import task_suite as chain_task_suite
from agentdojo.default_suites.v1.chain.user_tasks import ChainUserTask  # noqa: F401 - Register tasks

__all__ = ["chain_task_suite"]

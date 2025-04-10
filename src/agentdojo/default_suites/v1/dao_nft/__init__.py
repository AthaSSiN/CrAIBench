from agentdojo.default_suites.v1.dao_nft.injection_tasks import DaoNftInjectionTask  # noqa: F401 - Register tasks
from agentdojo.default_suites.v1.dao_nft.task_suite import task_suite as dao_nft_task_suite
from agentdojo.default_suites.v1.dao_nft.user_tasks import DaoNftUserTask  # noqa: F401 - Register tasks

__all__ = ["dao_nft_task_suite"]

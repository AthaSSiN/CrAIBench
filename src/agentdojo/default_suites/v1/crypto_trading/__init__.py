from agentdojo.default_suites.v1.crypto_trading.injection_tasks import CryptoTradingInjectionTask  # noqa: F401 - Register tasks
from agentdojo.default_suites.v1.crypto_trading.task_suite import task_suite as crypto_trading_task_suite
from agentdojo.default_suites.v1.crypto_trading.user_tasks import CryptoTradingUserTask  # noqa: F401 - Register tasks

__all__ = ["crypto_trading_task_suite"]

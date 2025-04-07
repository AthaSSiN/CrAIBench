from agentdojo.default_suites.v1.tools.chain_client import (
    Wallet,
    getBalance,
    transfer,
    getTransactions,
    bridge,
    stake,
    deploy_token_contract,
    airdrop,
    secure_funds
)

from agentdojo.default_suites.v1.tools.file_reader import Filesystem, read_file

from agentdojo.functions_runtime import TaskEnvironment, make_function
from agentdojo.task_suite.task_suite import TaskSuite


class ChainEnvironment(TaskEnvironment):
    wallet: Wallet
    filesystem: Filesystem


TOOLS = [
    getBalance,
    transfer,
    getTransactions,
    bridge,
    stake,
    deploy_token_contract,
    airdrop,
    read_file,
    secure_funds
]

task_suite = TaskSuite[ChainEnvironment]("chain", ChainEnvironment, [make_function(tool) for tool in TOOLS])

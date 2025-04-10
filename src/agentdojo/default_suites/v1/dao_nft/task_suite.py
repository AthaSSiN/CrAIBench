from agentdojo.default_suites.v1.tools.dao_nft_client import (
    Wallet,
    contractInvocation,
    uploadToIPFS,
    proposeToDAO,
    voteOnDAO,
    createNFT,
    createMessage,
    deleteMessage,
    gibwork,
    secure_funds,
    get_transactions
)

from agentdojo.default_suites.v1.tools.file_reader import Filesystem, read_file

from agentdojo.functions_runtime import TaskEnvironment, make_function
from agentdojo.task_suite.task_suite import TaskSuite


class DaoNftEnvironment(TaskEnvironment):
    wallet: Wallet
    filesystem: Filesystem


TOOLS = [
    contractInvocation,
    uploadToIPFS,
    proposeToDAO,
    voteOnDAO,
    createNFT,
    createMessage,
    deleteMessage,
    gibwork,
    secure_funds,
    get_transactions,
    read_file
]


task_suite = TaskSuite[DaoNftEnvironment]("dao_nft", DaoNftEnvironment, [make_function(tool) for tool in TOOLS])




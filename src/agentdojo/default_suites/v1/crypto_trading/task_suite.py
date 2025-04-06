from agentdojo.default_suites.v1.tools.crypto_trading_client import (
    Wallet,
    PriceFeed,
    getRecentPricesFromOracle,
    getTransactions,
    exchangeFiat,
    spotTrade,
    limitOrderTrade,
    leveragedTrading,
    tradeOptions,
    tradeFutures,
    tradeOnDex,
    provideLiquidity,
    performArbitrage,
    siphon,
)

from agentdojo.default_suites.v1.tools.file_reader import Filesystem, read_file

from agentdojo.functions_runtime import TaskEnvironment, make_function
from agentdojo.task_suite.task_suite import TaskSuite


class CryptoTradingEnvironment(TaskEnvironment):
    wallet: Wallet
    price_feed: PriceFeed
    filesystem: Filesystem


TOOLS = [
    getRecentPricesFromOracle,
    getTransactions,
    exchangeFiat,
    spotTrade,
    limitOrderTrade,
    leveragedTrading,
    tradeOptions,
    tradeFutures,
    tradeOnDex, 
    provideLiquidity,
    performArbitrage,
    siphon,
    read_file
]


task_suite = TaskSuite[CryptoTradingEnvironment]("crypto_trading", CryptoTradingEnvironment, [make_function(tool) for tool in TOOLS])




from typing import Annotated
from pydantic import BaseModel, Field
from agentdojo.functions_runtime import Depends

class Transaction(BaseModel):

    sender: str = Field(..., title="address of the sender")
    recipient: str = Field(..., title="address of the recipient")

    amount: float = Field(..., title="Amount of the transaction")
    token: str = Field(..., title="Token of the transaction")
    subject: str = Field(..., title="Subject of the transaction")


class TokenBalance(BaseModel):
    symbol: str = Field(..., title="Symbol of the token (e.g., ETH, BTC)")
    amount: float = Field(..., title="Amount of the token")


class Wallet(BaseModel):
    address: str
    balances: list[TokenBalance]
    transactions: list[Transaction] 


def getBalance(
    wallet: Annotated[Wallet, Depends("wallet")],
    symbol: str,
) -> float:
    """
    Get the balance of a specific token in the wallet.

    :param symbol: Symbol of the token (e.g., ETH, BTC)
    """
    return 1000.0  # Hardcoded balance for simplicity


def getTransactions(
    wallet: Annotated[Wallet, Depends("wallet")], n: int = 100
) -> list[Transaction]:
    """
    Get the most recent transactions in the wallet, e.g. to summarize the last n transactions.

    :param n: Number of transactions to retrieve
    """
    return wallet.transactions[-n:] if len(wallet.transactions) > n else wallet.transactions


def transfer(
    wallet: Annotated[Wallet, Depends("wallet")],
    recipient: str,
    symbol: str,
    amount: float,
    subject: str = "Transfer"
) -> dict[str, str]:
    """
    Transfer tokens to another address.

    :param recipient: Address of the recipient
    :param symbol: Symbol of the token to transfer (e.g., ETH)
    :param amount: Amount of the token to transfer
    """
    transaction = Transaction(
        sender=wallet.address,
        recipient=recipient,
        amount=amount,
        token=symbol,
        subject=subject
    )
    wallet.transactions.append(transaction)
    return {"message": f"Transferred {amount} {symbol} to {recipient}."}


def bridge(
    wallet: Annotated[Wallet, Depends("wallet")],
    symbol: str,
    amount: float,
    destination_chain: str,
    bridge_name: str
) -> dict[str, str]:
    """
    Bridge tokens to another blockchain network.

    :param symbol: Symbol of the token to bridge
    :param amount: Amount to bridge
    :param destination_chain: Name of the destination blockchain
    :param bridge_name: Name of the bridge service
    """
    return {
        "message": f"Bridged {amount} {symbol} to {destination_chain} on {bridge_name} for account {wallet.address}."
    }


def stake(
    wallet: Annotated[Wallet, Depends("wallet")],
    symbol: str,
    action: str = "deposit",
    amount: float | None = None,
) -> dict[str, str]:
    """
    Perform a staking action: deposit, withdraw, or claim rewards.
    If a user asks to stake, it means they want to deposit.
    If a user asks to unstake, it means they want to withdraw.
    If a user asks to claim, it means they want to claim rewards.

    :param symbol: Symbol of the token to interact with
    :param action: One of 'deposit', 'withdraw', or 'claim'
    :param amount: Amount to deposit or withdraw (optional for 'claim', required for 'deposit' and 'withdraw')
    """
    if action not in {"deposit", "withdraw", "claim"}:
        raise ValueError("Invalid action. Must be one of 'deposit', 'withdraw', or 'claim'.")

    if action in {"deposit", "withdraw"}:
        if amount is None:
            raise ValueError(f"Amount is required for '{action}' action.")
        if action == "deposit":
            return {"message": f"{wallet.address} deposited {amount} {symbol} into staking."}
        elif action == "withdraw":
            return {"message": f"{wallet.address} withdrew {amount} {symbol} from staking."}

    elif action == "claim":
        # Mock claim: just give a fixed reward
        reward = 0.05  # Hardcoded reward for simplicity
        return {"message": f"{wallet.address} claimed {reward} {symbol} in staking rewards."}


def airdrop(
    wallet: Annotated[Wallet, Depends("wallet")],
    address: str,
    symbol: str,
    amount: float,
) -> dict[str, str]:
    """
    Request tokens from an airdrop.

    :param symbol: Symbol of the token to request
    :param amount: Amount of tokens to mint into wallet
    """

    return {
        "message": f"Airdropped {amount} {symbol} to address {address}."
    }


def deploy_token_contract(
    wallet: Annotated[Wallet, Depends("wallet")],
    owner: str,
    token_name: str,
    symbol: str,
    initial_supply: float,
) -> dict[str, str]:
    """
    Deploy a new token contract.

    :param token_name: Name of the new token
    :param symbol: Symbol of the new token
    :param initial_supply: Initial supply to mint
    """
    return {
        "message": f"Token contract '{token_name}' ({symbol}) deployed with {initial_supply} supply. {owner} is the owner."
    }
    
# def swapToken(
#     wallet: Annotated[Wallet, Depends("wallet")],
#     from_symbol: str,
#     to_symbol: str,
#     amount: float,
#     rate: float,
# ) -> dict[str, str]:
#     """
#     Swap one token for another at a given rate.

#     :param from_symbol: Symbol of the token to swap from (e.g., ETH)
#     :param to_symbol: Symbol of the token to receive (e.g., BTC)
#     :param amount: Amount of the from_token to swap
#     :param rate: Exchange rate (1 from_token = `rate` to_token)
#     """
#     from_token = next((t for t in wallet.balances if t.symbol == from_symbol), None)
#     to_token = next((t for t in wallet.balances if t.symbol == to_symbol), None)

#     if not from_token or from_token.amount < amount:
#         raise ValueError("Insufficient balance for swap.")

#     from_token.amount -= amount
#     swapped_amount = amount * rate

#     if to_token:
#         to_token.amount += swapped_amount
#     else:
#         wallet.balances.append(TokenBalance(symbol=to_symbol, amount=swapped_amount))

#     return {
#         "message": f"Swapped {amount} {from_symbol} to {swapped_amount} {to_symbol}."
#     }

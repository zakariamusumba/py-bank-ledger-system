from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple, Optional

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds"""
    def __init__(self, balance: float, amount: float, account_type: str = "Account"):
        self.balance = balance
        self.amount = amount
        self.account_type = account_type
        self.message = f"{account_type}: Insufficient funds. Balance: ${balance:.2f}, Requested: ${amount:.2f}"
        super().__init__(self.message)

class BankAccount(ABC):
    """Abstract base class for bank accounts with encapsulated balance"""
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0.0):
        """
        Initialize a bank account
        
        Args:
            account_number: Unique account identifier
            owner_name: Name of account holder
            initial_balance: Starting balance (must be non-negative)
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
            
        self._account_number = account_number
        self._owner_name = owner_name
        self._balance = initial_balance
        self._transaction_history: List[Tuple] = []
        self._created_at = datetime.now()
    
    @property
    def account_number(self) -> str:
        """Get account number (read-only)"""
        return self._account_number
    
    @property
    def owner_name(self) -> str:
        """Get owner name (read-only)"""
        return self._owner_name
    
    @property
    def balance(self) -> float:
        """Get current balance (read-only)"""
        return self._balance
    
    @property
    def transaction_history(self) -> List[Tuple]:
        """Get transaction history (read-only copy)"""
        return self._transaction_history.copy()
    
    def _record_transaction(self, transaction_type: str, amount: float, 
                           balance_after: float, description: str = "") -> None:
        """
        Record a transaction in the history
        
        Args:
            transaction_type: Type of transaction (deposit, withdrawal, etc.)
            amount: Transaction amount
            balance_after: Balance after transaction
            description: Optional description
        """
        timestamp = datetime.now()
        transaction = (timestamp, transaction_type, amount, balance_after, description)
        self._transaction_history.append(transaction)
    
    @abstractmethod
    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful
            
        Raises:
            InsufficientFundsError: If insufficient funds
        """
        pass
    
    def get_balance(self) -> float:
        return self._balance
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._account_number}, Owner: {self._owner_name}, Balance: ${self._balance:.2f})"
    
    def __repr__(self) -> str:
        return self.__str__()
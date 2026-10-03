from .base import BankAccount, InsufficientFundsError
from typing import Optional

class CheckingAccount(BankAccount):
    """Checking account with overdraft protection"""
    
    def __init__(self, account_number: str, owner_name: str, 
                 initial_balance: float = 0.0, overdraft_limit: float = 500.0,
                 overdraft_penalty: float = 35.0):
        """
        Initialize a checking account
        
        Args:
            account_number: Unique account identifier
            owner_name: Name of account holder
            initial_balance: Starting balance
            overdraft_limit: Maximum overdraft allowed
            overdraft_penalty: Penalty for using overdraft
        """
        super().__init__(account_number, owner_name, initial_balance)
        self._overdraft_limit = overdraft_limit
        self._overdraft_penalty = overdraft_penalty
    
    @property
    def overdraft_limit(self) -> float:
        """Get overdraft limit"""
        return self._overdraft_limit
    
    @property
    def overdraft_penalty(self) -> float:
        """Get overdraft penalty"""
        return self._overdraft_penalty
    
    @property
    def available_balance(self) -> float:
        """Get available balance including overdraft"""
        return self._balance + self._overdraft_limit
    
    def deposit(self, amount: float) -> bool:
        """
        Deposit money into checking account
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If amount is invalid
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        self._record_transaction("deposit", amount, self._balance, "Checking deposit")
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from checking account with overdraft protection
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If amount is invalid
            InsufficientFundsError: If withdrawal exceeds available balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        # Check if withdrawal would exceed overdraft limit
        if amount > self.available_balance:
            raise InsufficientFundsError(
                self.available_balance, 
                amount, 
                "Checking Account (with overdraft)"
            )
        
        # Check if this withdrawal will trigger overdraft
        will_overdraft = (self._balance - amount) < 0
        
        self._balance -= amount
        
        # Apply penalty if overdraft is triggered
        if will_overdraft:
            self._balance -= self._overdraft_penalty
            self._record_transaction(
                "withdrawal", 
                amount, 
                self._balance, 
                f"Checking withdrawal (OVERDRAFT - ${self._overdraft_penalty:.2f} penalty)"
            )
            self._record_transaction(
                "penalty", 
                self._overdraft_penalty, 
                self._balance, 
                "Overdraft penalty"
            )
        else:
            self._record_transaction("withdrawal", amount, self._balance, "Checking withdrawal")
        
        return True
    
    def __str__(self) -> str:
        return (f"CheckingAccount({self._account_number}, Owner: {self._owner_name}, "
                f"Balance: ${self._balance:.2f}, Overdraft Limit: ${self._overdraft_limit:.2f}, "
                f"Available: ${self.available_balance:.2f})")
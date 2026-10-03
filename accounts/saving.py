from .base import BankAccount, InsufficientFundsError
from datetime import datetime, timedelta
import math
from typing import Optional

class SavingsAccount(BankAccount):
    
    def __init__(self, account_number: str, owner_name: str, 
                 initial_balance: float = 0.0, interest_rate: float = 0.02,
                 minimum_balance: float = 100.0):
        super().__init__(account_number, owner_name, initial_balance)
        self._interest_rate = interest_rate
        self._minimum_balance = minimum_balance
        self._last_interest_date = datetime.now()
    
    @property
    def interest_rate(self) -> float:
        return self._interest_rate
    
    @property
    def minimum_balance(self) -> float:
        return self._minimum_balance
    
    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        self._record_transaction("deposit", amount, self._balance, "Savings deposit")
        return True
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self._balance - amount < self._minimum_balance:
            raise InsufficientFundsError(
                self._balance - self._minimum_balance, 
                amount, 
                "Savings Account"
            )
        
        self._balance -= amount
        self._record_transaction("withdrawal", amount, self._balance, "Savings withdrawal")
        return True
    
    def calculate_compound_interest(self, days: Optional[int] = None) -> float:
        if days is None:
            days = (datetime.now() - self._last_interest_date).days
        
        if days <= 0:
            return 0.0
        
        P = self._balance  # Principal
        r = self._interest_rate  # Annual interest rate
        n = 365  # Compounding frequency (daily)
        t = days / 365  # Time in years
        A = P * math.pow(1 + r/n, n * t)
        interest = A - P
        
        return interest
    
    def apply_interest(self, days: Optional[int] = None) -> float:
        interest = self.calculate_compound_interest(days)
        
        if interest > 0:
            self._balance += interest
            self._last_interest_date = datetime.now()
            self._record_transaction(
                "interest", 
                interest, 
                self._balance, 
                f"Compound interest applied ({days or 'auto'} days)"
            )
        
        return interest
    
    def __str__(self) -> str:
        return (f"SavingsAccount({self._account_number}, Owner: {self._owner_name}, "
                f"Balance: ${self._balance:.2f}, Rate: {self._interest_rate*100:.1f}%, "
                f"Min: ${self._minimum_balance:.2f})")
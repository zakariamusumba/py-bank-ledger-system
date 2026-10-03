from datetime import datetime
from typing import List, Tuple, Optional
from accounts.base import BankAccount

class TransactionLedger:
    
    def __init__(self):
        self._transactions: List[Tuple] = []
        self._transaction_counter = 0
    
    def record_transaction(self, from_account: Optional[BankAccount], 
                          to_account: Optional[BankAccount],
                          amount: float, 
                          transaction_type: str,
                          description: str = "") -> int:
        self._transaction_counter += 1
        transaction_id = self._transaction_counter
        timestamp = datetime.now()
        
        from_acc_num = from_account.account_number if from_account else "EXTERNAL"
        to_acc_num = to_account.account_number if to_account else "EXTERNAL"
        
        transaction = (
            transaction_id,
            timestamp,
            transaction_type,
            from_acc_num,
            to_acc_num,
            amount,
            description
        )
        
        self._transactions.append(transaction)
        return transaction_id
    
    def transfer(self, from_account: BankAccount, to_account: BankAccount, 
                amount: float, description: str = "") -> bool:
        from_account.withdraw(amount)
        
        try:
            to_account.deposit(amount)
            self.record_transaction(
                from_account, 
                to_account, 
                amount, 
                "transfer",
                description or f"Transfer from {from_account.account_number} to {to_account.account_number}"
            )
            
            return True
            
        except Exception as e:
            from_account.deposit(amount)
            raise e
    
    def get_transactions(self) -> List[Tuple]:
        return self._transactions.copy()
    
    def get_account_transactions(self, account: BankAccount) -> List[Tuple]:
        account_num = account.account_number
        return [
            t for t in self._transactions 
            if t[3] == account_num or t[4] == account_num
        ]
    
    def get_transaction_summary(self) -> dict:
        if not self._transactions:
            return {
                "total_transactions": 0,
                "total_transferred": 0.0,
                "total_deposits": 0.0,
                "total_withdrawals": 0.0
            }
        
        total_transferred = sum(t[5] for t in self._transactions if t[2] == "transfer")
        total_deposits = sum(t[5] for t in self._transactions if t[2] == "deposit")
        total_withdrawals = sum(t[5] for t in self._transactions if t[2] == "withdrawal")
        
        return {
            "total_transactions": len(self._transactions),
            "total_transferred": total_transferred,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals
        }
    
    def print_audit_trail(self, account: Optional[BankAccount] = None) -> None:
        transactions = (
            self.get_account_transactions(account) if account 
            else self.get_transactions()
        )
        
        print("\n" + "="*100)
        print("TRANSACTION LEDGER AUDIT TRAIL")
        print("="*100)
        
        if account:
            print(f"Account: {account.account_number} ({account.owner_name})")
            print("-"*100)
        
        if not transactions:
            print("No transactions found.")
            return
        
        print(f"{'ID':<5} {'Timestamp':<20} {'Type':<12} {'From':<15} {'To':<15} {'Amount':<12} {'Description':<30}")
        print("-"*100)
        
        for trans in transactions:
            trans_id, timestamp, trans_type, from_acc, to_acc, amount, desc = trans
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{trans_id:<5} {timestamp_str:<20} {trans_type:<12} {from_acc:<15} {to_acc:<15} "
                  f"${amount:>10.2f}  {desc[:30]:<30}")
        
        print("="*100)
        summary = self.get_transaction_summary()
        print(f"Summary: {summary['total_transactions']} transactions | "
              f"Transferred: ${summary['total_transferred']:.2f} | "
              f"Deposits: ${summary['total_deposits']:.2f} | "
              f"Withdrawals: ${summary['total_withdrawals']:.2f}")
        print("="*100 + "\n")
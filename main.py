#!/usr/bin/env python3
"""
Financial Account Management System
Demonstrates OOP principles: inheritance, polymorphism, encapsulation
"""

from accounts import SavingsAccount, CheckingAccount, InsufficientFundsError
from services import TransactionLedger
import time


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)


def print_account_info(account, title: str = "Account Information"):
    """Print account details"""
    print(f"\n{title}:")
    print(f"  Type: {type(account).__name__}")
    print(f"  Account #: {account.account_number}")
    print(f"  Owner: {account.owner_name}")
    print(f"  Balance: ${account.balance:,.2f}")
    
    if hasattr(account, 'available_balance'):
        print(f"  Available (with overdraft): ${account.available_balance:,.2f}")
    if hasattr(account, 'minimum_balance'):
        print(f"  Minimum Balance: ${account.minimum_balance:,.2f}")
    if hasattr(account, 'interest_rate'):
        print(f"  Interest Rate: {account.interest_rate*100:.2f}%")


def simulate_transfers(savings, checking, ledger):
    """Simulate various transfer scenarios"""
    print_section("SIMULATING CROSS-ACCOUNT TRANSFERS")
    
    # Scenario 1: Successful transfer from savings to checking
    print("\n1. Transfer $500 from Savings to Checking:")
    try:
        ledger.transfer(savings, checking, 500, "Monthly transfer")
        print(f"   ✓ Transfer successful!")
        print(f"   Savings balance: ${savings.balance:,.2f}")
        print(f"   Checking balance: ${checking.balance:,.2f}")
    except InsufficientFundsError as e:
        print(f"   ✗ Transfer failed: {e}")
    
    # Scenario 2: Transfer from checking to savings
    print("\n2. Transfer $200 from Checking to Savings:")
    try:
        ledger.transfer(checking, savings, 200, "Savings deposit")
        print(f"   ✓ Transfer successful!")
        print(f"   Checking balance: ${checking.balance:,.2f}")
        print(f"   Savings balance: ${savings.balance:,.2f}")
    except InsufficientFundsError as e:
        print(f"   ✗ Transfer failed: {e}")
    
    # Scenario 3: Attempt large withdrawal that triggers overdraft
    print("\n3. Attempt to withdraw $1,800 from Checking (triggers overdraft):")
    try:
        checking.withdraw(1800)
        print(f"   ✓ Withdrawal successful (with overdraft)!")
        print(f"   Checking balance: ${checking.balance:,.2f}")
        print(f"   Note: Overdraft penalty of ${checking.overdraft_penalty:.2f} applied")
    except InsufficientFundsError as e:
        print(f"   ✗ Withdrawal failed: {e}")
    
    # Scenario 4: Attempt withdrawal that exceeds overdraft limit
    print("\n4. Attempt to withdraw $1,000 from Checking (exceeds overdraft limit):")
    try:
        checking.withdraw(1000)
        print(f"   ✓ Withdrawal successful!")
    except InsufficientFundsError as e:
        print(f"   ✗ Withdrawal failed: {e}")
        print(f"   Available balance: ${checking.available_balance:,.2f}")
    
    # Scenario 5: Attempt withdrawal that violates savings minimum
    print("\n5. Attempt to withdraw $1,500 from Savings (violates minimum balance):")
    try:
        savings.withdraw(1500)
        print(f"   ✓ Withdrawal successful!")
    except InsufficientFundsError as e:
        print(f"   ✗ Withdrawal failed: {e}")
        print(f"   Minimum balance requirement: ${savings.minimum_balance:,.2f}")


def apply_interest_demo(savings):
    """Demonstrate interest calculation"""
    print_section("INTEREST CALCULATION (Compound Interest)")
    
    print(f"\nCurrent Savings Balance: ${savings.balance:,.2f}")
    print(f"Annual Interest Rate: {savings.interest_rate*100:.2f}%")
    print(f"Compounding: Daily (n=365)")
    
    # Calculate interest for different periods
    for days in [30, 90, 365]:
        interest = savings.calculate_compound_interest(days)
        print(f"\n  Interest for {days} days: ${interest:,.2f}")
        print(f"  Formula: A = P(1 + r/n)^(nt)")
        print(f"           P = ${savings.balance:,.2f}, r = {savings.interest_rate}, n = 365, t = {days/365:.4f}")
    
    # Apply 30 days of interest
    print("\n  Applying 30 days of interest to account...")
    interest_applied = savings.apply_interest(30)
    print(f"  ✓ Interest applied: ${interest_applied:,.2f}")
    print(f"  New balance: ${savings.balance:,.2f}")


def demonstrate_polymorphism(accounts):
    """Demonstrate polymorphic behavior with different account types"""
    print_section("POLYMORPHISM DEMONSTRATION")
    
    print("\nProcessing deposits polymorphically:")
    for account in accounts:
        print(f"\n  {type(account).__name__} ({account.account_number}):")
        initial = account.balance
        account.deposit(100)
        print(f"    Deposited $100.00")
        print(f"    Balance: ${initial:,.2f} → ${account.balance:,.2f}")


def main():
    """Main function demonstrating the financial system"""
    
    print("\n" + "="*80)
    print(" FINANCIAL ACCOUNT MANAGEMENT SYSTEM ".center(80, "="))
    print("="*80)
    
    # Create accounts
    print_section("CREATING ACCOUNTS")
    
    savings = SavingsAccount(
        account_number="SAV-001",
        owner_name="Alice Johnson",
        initial_balance=5000.00,
        interest_rate=0.025,  # 2.5% annual
        minimum_balance=500.00
    )
    
    checking = CheckingAccount(
        account_number="CHK-001",
        owner_name="Alice Johnson",
        initial_balance=1500.00,
        overdraft_limit=500.00,
        overdraft_penalty=35.00
    )
    
    savings2 = SavingsAccount(
        account_number="SAV-002",
        owner_name="Bob Smith",
        initial_balance=10000.00,
        interest_rate=0.030,
        minimum_balance=1000.00
    )
    
    accounts = [savings, checking, savings2]
    
    # Display account information
    for account in accounts:
        print_account_info(account)
    
    # Initialize ledger
    ledger = TransactionLedger()
    
    # Simulate transfers
    simulate_transfers(savings, checking, ledger)
    
    # Demonstrate polymorphism
    demonstrate_polymorphism(accounts)
    
    # Apply interest
    apply_interest_demo(savings)
    
    # Additional transfer involving second savings account
    print_section("ADDITIONAL TRANSFERS")
    print("\nTransfer $2,000 from Bob's Savings to Alice's Checking:")
    try:
        ledger.transfer(savings2, checking, 2000, "Loan repayment")
        print(f"   ✓ Transfer successful!")
        print(f"   Bob's Savings: ${savings2.balance:,.2f}")
        print(f"   Alice's Checking: ${checking.balance:,.2f}")
    except InsufficientFundsError as e:
        print(f"   ✗ Transfer failed: {e}")
    
    # Display final balances
    print_section("FINAL ACCOUNT BALANCES")
    for account in accounts:
        print_account_info(account)
    
    # Print audit trail
    print_section("AUDIT TRAIL")
    ledger.print_audit_trail()
    
    # Print individual account statements
    print_section("INDIVIDUAL ACCOUNT STATEMENTS")
    for account in accounts:
        ledger.print_audit_trail(account)
    
    # Summary statistics
    print_section("SYSTEM SUMMARY")
    summary = ledger.get_transaction_summary()
    print(f"\nTotal Transactions: {summary['total_transactions']}")
    print(f"Total Amount Transferred: ${summary['total_transferred']:,.2f}")
    print(f"Total Deposits: ${summary['total_deposits']:,.2f}")
    print(f"Total Withdrawals: ${summary['total_withdrawals']:,.2f}")
    
    total_balance = sum(acc.balance for acc in accounts)
    print(f"\nTotal Balance Across All Accounts: ${total_balance:,.2f}")
    
    print("\n" + "="*80)
    print(" SIMULATION COMPLETE ".center(80, "="))
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
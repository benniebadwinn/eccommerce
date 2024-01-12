from account.models import Wallet
from django.db.models import Sum  # Import the Sum function



def get_user_wallet_balance(user):
    try:
        # Calculate the sum of wallet transactions for the user
        deposits = Wallet.objects.filter(user=user, transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        withdrawals = Wallet.objects.filter(user=user, transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate the sum of purchase transactions
        purchases = Wallet.objects.filter(user=user, transaction_type='purchase').aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate the wallet balance
        wallet_balance = deposits - withdrawals + purchases

        print(f"Deposits: {deposits}")
        print(f"Withdrawals: {withdrawals}")
        print(f"Purchases: {purchases}")
        print(f"Wallet Balance: {wallet_balance}")

        return wallet_balance
    except Exception as e:
        print(f"Error in get_user_wallet_balance: {e}")
        return 0
 
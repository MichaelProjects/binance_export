from .models import Order

def get_orders(transactions: list):
    orders = []
    for transaction_list in transactions:
        for transaction in transaction_list:
            order = Order.from_json(transaction)
            orders.append(order)

    for x in orders:
        print(x)


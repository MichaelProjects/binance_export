from dataclasses import dataclass


@dataclass(init=True, repr=True)
class Order:
    order_id: int
    symbol: str
    amount: float
    is_buy: bool
    fee: float
    price: float
    timestamp: str

    @staticmethod
    def from_json(data: dict):
        return Order(
            order_id=data['orderId'],
            symbol=data['symbol'],
            amount=data['executedQty'],
            is_buy=False if data["side"] == "SELL" else True,
            fee=0,
            price=data["price"],
            timestamp=data['time']
        )

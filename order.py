class Order:
    def __init__(self, agent_id, order_type, price, quantity, ttl=10):
        self.agent_id = agent_id
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.ttl = ttl

    def decrement_ttl(self):
        self.ttl -= 1
        return self.ttl <= 0
import random
from order import Order

class Agent:
    def __init__(self, agent_id, cash, assets):
        self.agent_id = agent_id
        self.cash = cash
        self.assets = assets

    def decide_action(self, market):
        # This method is overridden by subclasses
        pass

class RandomAgent(Agent):
    def decide_action(self, market):
        action = random.choice(['buy', 'sell'])
        price_variation = market.last_traded_price * 0.05
        price = round(random.uniform(market.last_traded_price - price_variation, market.last_traded_price + price_variation), 1)

        # For buying or selling, use a randomized quantity similar to previous logic
        if action == 'buy' and self.cash > 0:
            max_affordable_quantity = self.cash // price  # Use the randomized price here
            quantity = random.randint(1, max(1, max_affordable_quantity))
            if quantity > 0:
                self.cash -= quantity * price
                order = Order(self.agent_id, 'buy', price, quantity)
                market.add_order(order)
        elif action == 'sell' and self.assets > 0:
            quantity = random.randint(1, self.assets)
            self.assets -= quantity
            order = Order(self.agent_id, 'sell', price, quantity)
            market.add_order(order)
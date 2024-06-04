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
    def __init__(self, agent_id, cash, assets, trading_frequency=1.0):
        super().__init__(agent_id, cash, assets)
        self.trading_frequency = trading_frequency
    
    def decide_action(self, market, verbose=True):
        # Just exit and move on if the agent isn't trading this turn
        if random.random() > self.trading_frequency:
            return
        
        action = random.choice(['buy', 'sell'])
        price_variation = market.last_traded_price * 0.05
        price = round(random.uniform(market.last_traded_price - price_variation, market.last_traded_price + price_variation), 3)

        # Make a trade with a randomized price and quantity based on the last traded price and amount of cash/assets on hand
        if action == 'buy' and self.cash > 0:
            max_affordable_quantity = self.cash // price
            quantity = random.randint(1, max(1, max_affordable_quantity))
            if quantity > 0:
                self.cash -= quantity * price
                order = Order(self.agent_id, 'buy', price, quantity)
                market.add_order(order, verbose=verbose)
        
        elif action == 'sell' and self.assets > 0:
            quantity = random.randint(1, self.assets)
            if quantity > 0:
                self.assets -= quantity
                order = Order(self.agent_id, 'sell', price, quantity)
                market.add_order(order, verbose=verbose)
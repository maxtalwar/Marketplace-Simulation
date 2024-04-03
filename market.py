import random

class Order:
    def __init__(self, agent_id, order_type, price, quantity):
        self.agent_id = agent_id
        self.order_type = order_type  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity

class Market:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def get_agent_orders(self, agent_id):
        buy_orders = [order for order in self.buy_orders if order.agent_id == agent_id]
        sell_orders = [order for order in self.sell_ordrs if order_agent_id == agent_id]

        return {"Buy": buy_orders,
                "Sell": sell_orders}

    def add_order(self, order):
        # Combine similar orders
        same_type_orders = self.buy_orders if order.order_type == 'buy' else self.sell_orders
        for existing_order in same_type_orders:
            if existing_order.agent_id == order.agent_id and existing_order.price == order.price:
                existing_order.quantity += order.quantity
                print(f"Agent {order.agent_id} increased their {order.order_type} order by {order.quantity} units at {order.price} per unit. New total quantity: {existing_order.quantity}.")
                self.match_orders()
                return
            
        # Reduce opposite orders
        opposite_orders = self.sell_orders if order.order_type == 'buy' else self.buy_orders
        for opposite_order in opposite_orders:
            if opposite_order.agent_id == order.agent_id and opposite_order.price == order.price:
                if opposite_order.quantity > order.quantity:
                    opposite_order.quantity -= order.quantity
                    print(f"Agent {order.agent_id} reduced their {opposite_order.order_type} order by {order.quantity} units at {order.price} per unit. New total quantity: {opposite_order.quantity}.")
                    self.match_orders()
                    return
                else:
                    order.quantity -= opposite_order.quantity
                    print(f"Agent {order.agent_id} cancelled their {opposite_order.order_type} order of {opposite_order.quantity} units at {opposite_order.price} per unit.")
                    opposite_orders.remove(opposite_order)

        # Add the order if it wasn't aggregated or fully adjusted
        if order.quantity > 0:
            same_type_orders.append(order)
            print(f"Agent {order.agent_id} posted a new {order.order_type} order for {order.quantity} units at {order.price} per unit.")

        self.match_orders()

    def match_orders(self):
        # Ensure the buy orders are in descending price order and sell orders in ascending price order
        self.buy_orders.sort(key=lambda x: x.price, reverse=True)
        self.sell_orders.sort(key=lambda x: x.price)

        # Match orders from different agents
        i = 0
        while i < len(self.buy_orders):
            buy_order = self.buy_orders[i]
            matched = False
            for j, sell_order in enumerate(self.sell_orders):
                if buy_order.price >= sell_order.price:
                    executed_quantity = min(buy_order.quantity, sell_order.quantity)
                    buy_order.quantity -= executed_quantity
                    sell_order.quantity -= executed_quantity

                    print(f"Executing trade: {executed_quantity} units at {sell_order.price} per unit between agent {buy_order.agent_id} (buyer) and agent {sell_order.agent_id} (seller)")

                    if sell_order.quantity == 0:
                        self.sell_orders.pop(j)
                    if buy_order.quantity == 0:
                        self.buy_orders.pop(i)
                        i -= 1  # Adjust the index to account for the removal
                        break  # Break since this buy order is fully matched
                    
                    matched = True
            if not matched:
                i += 1  # Only increment if no match was made to avoid skipping orders

    def print_order_book(self):
        print("Order Book:")
        for order in self.buy_orders + self.sell_orders:
            print(f"Agent {order.agent_id} {order.order_type.capitalize()} order - Price: {order.price}, Quantity: {order.quantity}")
        if not self.buy_orders and not self.sell_orders:
            print("Order Book is currently empty.")

class Agent:
    def __init__(self, agent_id, cash=1000, assets=0):
        self.agent_id = agent_id
        self.cash = cash  # Starting cash
        self.assets = assets  # Starting assets

    def decide_action(self, market):
        # Determine the action type: 'buy' or 'sell'
        action = random.choice(['buy', 'sell'])

        # For buying, the quantity is influenced by the amount of cash available
        if action == 'buy':
            max_affordable_quantity = self.cash // 10  # Assuming a price of 10 for simplicity
            # Choose a random quantity up to the maximum affordable, influenced by available cash
            quantity = random.randint(1, max(1, max_affordable_quantity))
            if quantity > 0:
                self.cash -= quantity * 10  # Update cash to reflect the purchase intent
                order = Order(self.agent_id, 'buy', price=10, quantity=quantity)
                market.add_order(order)

        # For selling, the quantity is influenced by the number of assets held
        elif action == 'sell' and self.assets > 0:
            # Choose a random quantity up to the maximum available assets
            quantity = random.randint(1, self.assets)
            self.assets -= quantity  # Update assets to reflect the selling intent
            order = Order(self.agent_id, 'sell', price=10, quantity=quantity)
            market.add_order(order)

def simulate(market, agents, num_turns=10):
    for turn in range(num_turns):
        print(f"\nTurn {turn+1}")
        for agent in agents:
            agent.decide_action(market)
        # The market now automatically matches orders when they are added,
        # so there's no need to call an explicit execute_orders() method here.
        market.print_order_book()

market = Market()
agents = [
    Agent(agent_id=0, cash=500, assets=50),  # This agent starts with assets and can sell
    Agent(agent_id=1, cash=1000),  # This agent starts with cash and is more likely to buy
    Agent(agent_id=2, cash=900, assets=10)
]

simulate(market, agents)

from agents import RandomAgent
from order import Order

class Market:
    def __init__(self, starting_asset_price, agents):
        self.buy_orders = []
        self.sell_orders = []
        self.last_traded_price = starting_asset_price
        self.price_history = [self.last_traded_price]
        self.cash_history = []
        self.asset_history = []
        self.agents = agents

    def update_market_state(self, agents):
        # Sum all cash and assets from all agents to get total market values
        total_cash = sum(agent.cash for agent in agents)
        total_assets = sum(agent.assets for agent in agents)
        
        # Update histories
        self.cash_history.append(total_cash)
        self.asset_history.append(total_assets)

    def remove_order(self, order):
        if order.order_type == 'buy':
            self.buy_orders.remove(order)
        elif order.order_type == 'sell':
            self.sell_orders.remove(order)

    def get_agent_orders(self, agent_id):
        buy_orders = [order for order in self.buy_orders if order.agent_id == agent_id]
        sell_orders = [order for order in self.sell_ordrs if order.agent_id == agent_id]

        return {"Buy": buy_orders,
                "Sell": sell_orders}

    def add_order(self, order, verbose=True):
        # Combine similar orders
        same_type_orders = self.buy_orders if order.order_type == 'buy' else self.sell_orders
        for existing_order in same_type_orders:
            if existing_order.agent_id == order.agent_id and existing_order.price == order.price:
                existing_order.quantity += order.quantity
                if verbose: print(f"Agent {order.agent_id} increased their {order.order_type} order by {order.quantity} units at {order.price} per unit. New total quantity: {existing_order.quantity}.")
                return
            
        # Reduce opposite orders
        opposite_orders = self.sell_orders if order.order_type == 'buy' else self.buy_orders
        for opposite_order in opposite_orders:
            if opposite_order.agent_id == order.agent_id and opposite_order.price == order.price:
                if opposite_order.quantity > order.quantity:
                    opposite_order.quantity -= order.quantity
                    if verbose: print(f"Agent {order.agent_id} reduced their {opposite_order.order_type} order by {order.quantity} units at {order.price} per unit. New total quantity: {opposite_order.quantity}.")
                    return
                else:
                    order.quantity -= opposite_order.quantity
                    if verbose: print(f"Agent {order.agent_id} cancelled their {opposite_order.order_type} order of {opposite_order.quantity} units at {opposite_order.price} per unit.")
                    opposite_orders.remove(opposite_order)

        # Process any orders that haven't been already processed (aggregated or used to reduce a previous order)
        if order.quantity > 0:
            same_type_orders.append(order)
            if verbose: print(f"Agent {order.agent_id} posted a new {order.order_type} order for {order.quantity} units at {order.price} per unit.")
            self.match_order(order, verbose=verbose)

    def match_order(self, new_order, verbose=True):
        if new_order.order_type == 'sell':
            # For a sell order, find the highest priced buy order
            highest_buy = max(self.buy_orders, key=lambda x: x.price, default=None)

            while highest_buy and highest_buy.price >= new_order.price and new_order.quantity > 0:
                price = highest_buy.price
                self.execute_trade(highest_buy, new_order, price, verbose=verbose)
                
                highest_buy = max(self.buy_orders, key=lambda x: x.price, default=None)

        elif new_order.order_type == 'buy':
            # For a buy order, find the lowest priced sell order
            lowest_sell = min(self.sell_orders, key=lambda x: x.price, default=None)

            while lowest_sell and lowest_sell.price <= new_order.price and new_order.quantity > 0:
                price = lowest_sell.price
                self.execute_trade(new_order, lowest_sell, price, verbose=verbose)

                lowest_sell = min(self.sell_orders, key=lambda x: x.price, default=None)

    def execute_trade(self, buy_order, sell_order, price, verbose=True):
        executed_quantity = min(buy_order.quantity, sell_order.quantity)
        
        # Calculate the total cost of the trade
        total_trade_cost = executed_quantity * price
        
        # Find the buyer and seller agents based on agent_id
        buyer = next((agent for agent in self.agents if agent.agent_id == buy_order.agent_id), None)
        seller = next((agent for agent in self.agents if agent.agent_id == sell_order.agent_id), None)
        
        if buyer and seller:
            # Transfer cash from buyer to seller
            buyer.cash -= total_trade_cost
            seller.cash += total_trade_cost

            # Transfer assets from seller to buyer
            seller.assets -= executed_quantity
            buyer.assets += executed_quantity

            if verbose:
                print(f"Executing trade: {executed_quantity} units at {price} per unit between buyer {buyer.agent_id} and seller {seller.agent_id}")
                print(f"Cash transferred: {total_trade_cost} from buyer {buyer.agent_id} to seller {seller.agent_id}")
                print(f"Assets transferred: {executed_quantity} units from seller {seller.agent_id} to buyer {buyer.agent_id}")

        # Adjust quantities in the order book
        buy_order.quantity -= executed_quantity
        sell_order.quantity -= executed_quantity

        # Update last traded price
        self.last_traded_price = price

        # Remove fulfilled orders from the order book
        if buy_order.quantity == 0:
            self.remove_order(buy_order)
        if sell_order.quantity == 0:
            self.remove_order(sell_order)


    def match_orders(self, verbose=True):
        # Ensure the buy orders are in descending price order and sell orders in ascending price order
        self.buy_orders.sort(key=lambda x: x.price, reverse=True)
        self.sell_orders.sort(key=lambda x: x.price)

        # Match orders from different agents
        i = 0
        while i < len(self.buy_orders):
            try:
                buy_order = self.buy_orders[i]
            except IndexError:
                if verbose: print("IndexError caught: 'i' is out of range.", "i:", i, "buy_orders:", self.buy_orders)
                break
                
            matched = False
            for j, sell_order in enumerate(self.sell_orders):
                if buy_order.price >= sell_order.price:
                    executed_quantity = min(buy_order.quantity, sell_order.quantity)
                    buy_order.quantity -= executed_quantity
                    sell_order.quantity -= executed_quantity

                    if verbose: print(f"Executing trade: {executed_quantity} units at {sell_order.price} per unit between agent {buy_order.agent_id} (buyer) and agent {sell_order.agent_id} (seller)")
                    self.last_traded_price = sell_order.price

                    if sell_order.quantity == 0:
                        self.sell_orders.pop(j)
                    if buy_order.quantity == 0:
                        self.buy_orders.pop(i)
                        i -= 1  # Adjust the index to account for the removal
                        break  # Break since this buy order is fully matched

                    if len(self.buy_orders) == 0:
                        print("Buy orders list is empty. Exiting loop.")
                        break
                    
                    matched = True
            if not matched:
                i += 1  # Only increment if no match was made to avoid skipping orders

    def print_orderbook_detailed(self):
        print("Order Book:")
        for order in self.buy_orders + self.sell_orders:
            print(f"Agent {order.agent_id} {order.order_type.capitalize()} order - Price: {order.price}, Quantity: {order.quantity}")
        if not self.buy_orders and not self.sell_orders:
            print("Order Book is currently empty.")

    def print_orderbook_basic(market):
        # Aggregate buy orders by price
        buy_aggregated = {}
        for order in market.buy_orders:
            buy_aggregated[order.price] = buy_aggregated.get(order.price, 0) + order.quantity

        # Aggregate sell orders by price
        sell_aggregated = {}
        for order in market.sell_orders:
            sell_aggregated[order.price] = sell_aggregated.get(order.price, 0) + order.quantity

        # Calculate total value for sell orders
        sell_total_value = sum(price * quantity for price, quantity in sell_aggregated.items())
        
        # Calculate total value for buy orders
        buy_total_value = sum(price * quantity for price, quantity in buy_aggregated.items())

        # Sort and prepare sell orders for display (descending, since sell orders will be displayed on top)
        sell_orders_sorted = sorted(sell_aggregated.items(), key=lambda x: x[0], reverse=True)
        
        # Sort and prepare buy orders for display (also descending to maintain the overall descending price order)
        buy_orders_sorted = sorted(buy_aggregated.items(), key=lambda x: x[0], reverse=True)

        # Visualize the order book
        print("\nOrder Book:")
        print(f"SELL ORDERS: (total value = {round(sell_total_value, 2)})")
        for price, quantity in sell_orders_sorted:
            print(f"Price: {price}, Quantity: {quantity}")

        print(f"\nBUY ORDERS: (total value = {round(buy_total_value, 2)})")
        for price, quantity in buy_orders_sorted:
            print(f"Price: {price}, Quantity: {quantity}")

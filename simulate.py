import matplotlib.pyplot as plt
from agents import RandomAgent
from market import Market

def simulate(market, agents, num_turns=10):
    for turn in range(num_turns-1):
        print(f"\nTurn {turn+1}")
        for agent in agents:
            agent.decide_action(market)
        market.print_order_book()
        market.price_history.append(market.last_traded_price)

market = Market()
agents = [
    RandomAgent(agent_id=0, cash=500, assets=50), # This agent is a middle ground
    RandomAgent(agent_id=1, cash=1000, assets=0),  # This agent starts with cash and is more likely to buy
    RandomAgent(agent_id=2, cash=0, assets=100) # This agent starts with assets and can sell
]

simulate(market, agents, num_turns=10)

print(market.price_history)
print(len(market.price_history))

plt.figure(figsize=(10, 6))
plt.plot(market.price_history, marker='o', linestyle='-')
plt.title('Asset Price Over Time')
plt.xlabel('Time Step')
plt.ylabel('Last Traded Price')
plt.grid(True)
plt.show()
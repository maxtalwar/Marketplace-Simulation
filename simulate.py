import matplotlib.pyplot as plt
from market import Market
from agent_populations import generate_random_agents

def simulate(market, agents, num_turns=10):
    for turn in range(num_turns-1):
        print(f"\nTurn {turn+1}")
        for agent in agents:
            agent.decide_action(market)
        market.print_order_book()
        market.price_history.append(market.last_traded_price)

market = Market()
agents = generate_random_agents(num_agents=3, starting_asset_price=10, total_value=1000)

simulate(market, agents, num_turns=50)

plt.figure(figsize=(10, 6))
plt.plot(market.price_history, marker='o', linestyle='-')
plt.title('Asset Price Over Time')
plt.xlabel('Time Step')
plt.ylabel('Last Traded Price')
plt.grid(True)
plt.show()
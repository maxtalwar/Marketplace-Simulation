import time
overall_start_time = time.time()

import_start_time = overall_start_time

import matplotlib.pyplot as plt
from market import Market
from agent_populations import generate_random_agents, generate_equal_agents

import_end_time = time.time()

def simulate(market, agents, num_turns=10):
    for turn in range(num_turns):
        print(f"\nTurn {turn+1}")
        for agent in agents:
            agent.decide_action(market)
        market.print_orderbook_basic()
        market.price_history.append(market.last_traded_price)

market = Market()
agents = generate_equal_agents(num_agents=50, starting_asset_price=10, total_value=1000)

simulation_start_time = time.time()

simulate(market, agents, num_turns=1000)

simulation_end_time = time.time()
overall_end_time = simulation_end_time

print(f"\nImporting packages took {round(import_end_time - import_start_time, 3)} seconds to complete.")
print(f"Trade simulations took {round(simulation_end_time - simulation_start_time, 3)} seconds to complete.")
print(f"Overall simulation took {round(simulation_end_time - overall_start_time, 3)} seconds to complete.")

plt.figure(figsize=(10, 6))
plt.plot(market.price_history, marker='o', linestyle='-')
plt.title('Asset Price Over Time')
plt.xlabel('Time Step')
plt.ylabel('Last Traded Price')
plt.grid(True)
plt.show()

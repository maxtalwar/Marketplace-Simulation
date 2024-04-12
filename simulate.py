# Import functions and test execution time of doing so
import time # I get that leaving out the import time action isn't ideal haha but I can't exactly import it after the next line
overall_start_time = time.time()

import_start_time = overall_start_time

import matplotlib.pyplot as plt
from market import Market
from agent_populations import generate_random_agents, generate_equal_agents, generate_base_agents

import_end_time = time.time()

def simulate(market, agents, num_turns=10, verbose=False):
    # Repeat
    for turn in range(num_turns):
        if verbose: print(f"\nTurn {turn+1}")

        for agent in agents:
            agent.decide_action(market, verbose=verbose)
        
        market.price_history.append(market.last_traded_price)

        if verbose: market.print_orderbook_basic()

def main(plot=True, verbose=True):
    # Starting simulation parameters

    # Agent parameters
    num_agents = 500
    total_value = 1000
    trading_frequency = 0.5
    cash = 500
    assets = 5000

    # Simulation parameters
    num_turns = 200
    starting_asset_price = 10

    # Generate agents and market
    market = Market(starting_asset_price=starting_asset_price)
    agents = generate_base_agents(num_agents=num_agents, cash=cash, assets=assets, trading_frequency=trading_frequency)

    # Measure the simulation execution time
    simulation_start_time = time.time()
    simulate(market, agents, num_turns=num_turns, verbose=verbose)
    simulation_end_time = time.time()
    overall_end_time = simulation_end_time

    # Show simulation timing data
    if verbose:
        print(f"\nImporting packages took {round(import_end_time - import_start_time, 3)} seconds to complete.")
        print(f"Trade simulations took {round(simulation_end_time - simulation_start_time, 3)} seconds to complete.")
        print(f"Overall simulation took {round(overall_end_time - overall_start_time, 3)} seconds to complete.")

    if plot:
        # Plot data
        plt.figure(figsize=(10, 6))
        plt.plot(market.price_history, marker='o', linestyle='-')
        plt.title('Asset Price Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('Last Traded Price')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()
# Import functions and test execution time of doing so
import time # I get that leaving out the import time action isn't ideal haha but I can't exactly import it after the next line
overall_start_time = time.time()

import_start_time = overall_start_time

import matplotlib.pyplot as plt
from market import Market
from agent_populations import generate_random_agents, generate_equal_agents, generate_base_agents

import_end_time = time.time()

def simulate(market, num_turns=10, verbose=False):
    # Repeat
    for turn in range(num_turns):
        total_cash = 0
        total_assets = 0

        if verbose: print(f"\nTurn {turn+1}")

        market.purge_old_orders(verbose=verbose)

        for agent in market.agents:
            agent.decide_action(market, verbose=verbose)

        market.update_market_state(market.agents)
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
    num_turns = 100
    starting_asset_price = .11

    # Generate agents and market
    agents = generate_base_agents(num_agents=num_agents, cash=cash, assets=assets, trading_frequency=trading_frequency)
    market = Market(starting_asset_price=starting_asset_price, agents=agents)

    # Measure the simulation execution time
    simulation_start_time = time.time()
    simulate(market, num_turns=num_turns, verbose=verbose)
    simulation_end_time = time.time()
    overall_end_time = simulation_end_time

    # Show simulation timing data
    if verbose:
        print(f"\nImporting packages took {round(import_end_time - import_start_time, 3)} seconds to complete.")
        print(f"Trade simulations took {round(simulation_end_time - simulation_start_time, 3)} seconds to complete.")
        print(f"Overall simulation took {round(overall_end_time - overall_start_time, 3)} seconds to complete.")

    if plot:
        plot_market_data(market)

def plot_market_data(market):
    plt.figure(figsize=(15, 12))  # Adjusted for better visibility

    # Plot price history
    plt.subplot(3, 2, 1)  # First row, first column
    plt.plot(market.price_history, marker='o', linestyle='-', color='blue')
    plt.title('Price History')
    plt.ylabel('Last Traded Price')
    plt.grid(True)

    # Plot total cash history
    plt.subplot(3, 2, 2)  # First row, second column
    plt.plot(market.cash_history, marker='o', linestyle='-', color='green')
    plt.title('Total Cash History')
    plt.ylabel('Total Cash in Market')
    plt.grid(True)

    # Plot circulating cash history
    plt.subplot(3, 2, 3)  # Second row, first column
    plt.plot(market.circulating_cash_history, marker='o', linestyle='-', color='green')
    plt.title('Circulating Cash History')
    plt.ylabel('Circulating Cash in Market')
    plt.grid(True)

    # Plot total asset history
    plt.subplot(3, 2, 4)  # Second row, second column
    plt.plot(market.asset_history, marker='o', linestyle='-', color='red')
    plt.title('Total Asset History')
    plt.ylabel('Total Assets in Market')
    plt.grid(True)

    # Plot circulating asset history
    plt.subplot(3, 2, 5)  # Third row, first column
    plt.plot(market.circulating_asset_history, marker='o', linestyle='-', color='red')
    plt.title('Circulating Asset History')
    plt.xlabel('Time Step')
    plt.ylabel('Circulating Assets in Market')
    plt.grid(True)

    plt.tight_layout()  # This ensures that the plots do not overlap
    plt.show()


if __name__ == "__main__":
    main()
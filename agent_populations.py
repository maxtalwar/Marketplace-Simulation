from agents import RandomAgent
import random

def generate_random_agents(num_agents=1000, starting_asset_price=10, total_value=1000, trading_frequency=1):
    agents = []
    for agent_index in range(num_agents):
        assets = random.randint(0, total_value // starting_asset_price)
        assets_value = assets * starting_asset_price
        cash = random.randint(0, total_value - assets_value)
        agents.append(RandomAgent(agent_id=agent_index, cash=cash, assets=assets, trading_frequency=trading_frequency))
    return agents


def generate_equal_agents(num_agents=1000):
    agents = []
    for agent_index in range(num_agents):
        assets = 50
        cash = 500
        trading_frequency = 1
        agents.append(RandomAgent(agent_id=agent_index, cash=cash, assets=assets, trading_frequency=trading_frequency))
    return agents


def generate_base_agents(num_agents=1000, cash=500, assets=50, trading_frequency=1):
    agents = [RandomAgent(agent_id=agent_index, cash=cash, assets=assets, trading_frequency=trading_frequency) for agent_index in range(num_agents)]
    return agents
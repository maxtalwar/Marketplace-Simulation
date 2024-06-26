# Marketplace Simulation
 
Author: Max Talwar

This project attempts to simulate a marketplace through an orderbook. Different custom agents can be plugged into the marketplace to interact with it in various ways (for example producers, consumers, speculators, etc), although some agents trade randomly to create the "noise" we would often see in various markets. It's currently a fairly isolated simulation, in the sense that it exists purely to simulate a marketplace. As it improves, though, the long-term vision is to use the marketplace as a tool for broader economics simulations that connects independent economic actors and allows them to trade.

To run this simulation, just run install the dependencies in the poetry lock file and run simulate.py!

## Agent Types

### Random Agent

The random agent is essentially the simplest actor in the simulation. It buys or sells a random quantity of units on any given turn based on the amount of resources it has at a random price within 5% of the last traded price. An interesting emergent feature of the random agent is that in a simulation with only random agents after a while liquidity dries up and trades stop executing; every agent has used up all their "free cash" or assets posting orders on the orderbook but they're all at prices that don't match, essentially causing the orderbook to freeze. Marketmakers or arbitrageurs could potentially alleviate that problem, but I haven't implemented it yet. 

Another interesting emergent feature: probably unsurprisingly, the price that the token reaches is a function of the number of tokens and the amount of cash given to each agent. The equilibrium price typically settles around a price that makes the value of the tokens circulating in the simulation equal to the value of the circulating cash in the simulation. For example, if each agent is given $500 in cash and 5000 tokens, the token price will settle at around $0.1. This isn't a hard and fast rule, and sometimes the final price settles a little above or below the theoretical equilibrium price, but the point is it always gets close. 
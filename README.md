# Marketplace Simulation
 
Author: Max Talwar

This project attempts to simulate a marketplace through an orderbook. Different custom agents can be plugged into the marketplace to interact with it in various ways (for example producers, consumers, speculators, etc), although some agents trade randomly to create the "noise" we would often see in various markets. It's currently a fairly isolated simulation, in the sense that it exists purely to simulate a marketplace. As it improves, though, the long-term vision is to use the marketplace as a tool for broader economics simulations that connects independent economic actors and allows them to trade.

## Agent Types

### Random Agent

The random agent is essentially the simplest actor in the simulation. It buys or sells a random quantity of units on any given turn based on the amount of resources it has at a random price within 5% of the last traded price. An interesting emergent feature of the random agent is that in a simulation with only random agents after a while liquidity dries up and trades stop executing; every agent has used up all their "free cash" or assets posting orders on the orderbook but they're all at prices that don't match, essentially causing the orderbook to freeze. Marketmakers or arbitrageurs could potentially alleviate that problem, but I haven't implemented it yet. 

Another interesting feature is that in a simulation with only random agents, the token price trends downward over time. The reason for this is because in a situation where agents are posting orders randomly and price is minimized, the lowest prices will be chosen over time. Here's an example: if the token's price is 10, one agent posts a sell order for 9.5, and another agent posts a buy order for 10.5, the trade will get filled at the cheapest price available: 9.5. So even though the skew of buy and sell orders above 10 was even, the price fell from 10 to 9.5. I'm not concerned about "fixing" this, because it's really just an emergent feature of these agents. 

<img width="997" alt="Random Agent Price Falling" src="https://github.com/maxtalwar/Marketplace-Simulation/assets/42502920/b9296515-1b26-49b8-a376-e1ab7a55fc28">

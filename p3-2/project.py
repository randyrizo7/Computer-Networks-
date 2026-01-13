"""
CPSC 5510, Seattle University, Project #3
Based on the Java version of Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""
import random

from network_simulator import NetworkSimulator

print('Network Simulator v1.0')

buffer = input('Enter trace level (>= 0): [0] ')
try:
    trace = int(buffer)
except ValueError:
    trace = 0
print('Trace level set to', trace)

buffer = input('Will the link change (Yes/No)? [No] ')
has_link_change = buffer.lower().strip().startswith('y')
print('Link will change:', 'Yes' if has_link_change else 'No')

buffer = input('Enter random seed: [random] ')
try:
    seed = int(buffer)
except ValueError:
    seed = random.randrange(int(1e14))
print('Random seed:', seed)

NetworkSimulator.run_simulator(has_link_change, trace, seed)

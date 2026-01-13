"""
CPSC 5510, Seattle University, Project #3
Based on the Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""


def to_layer_2(sender, receiver, minimum_costs):
    """
    Send notification from sender to receiver of sender's currently
    known minimum costs to sender to all other nodes.
    :param sender:        sender's node number
    :param receiver:      receiver's node number
    :param minimum_costs: sender's minimum cost to all nodes (a list indexed by
                          receivers' node numbers)
    """
    from packet import Packet
    from network_simulator import NetworkSimulator

    p = Packet(sender, receiver, minimum_costs)
    NetworkSimulator._to_layer_2(p)

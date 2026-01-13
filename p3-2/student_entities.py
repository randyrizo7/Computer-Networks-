"""
CPSC 5510, Seattle University, Project #3
:Author: Randy Rizo
version: s25
"""

# YOU MAY NOT ADD ANY IMPORTS
from entity import Entity
from student_utilities import to_layer_2



def common_init(self):
    """
    Kick off distance vector routing by setting up the distance table.

    Sets the initial row of the distance table using direct link costs, logs the 
    table, and sends the initial minimum cost vector to all neighbors.
    """
    self.distance_table = [[float('inf') for _ in range(4)] for _ in range(4)]
    print(f"entity {self.id}: initializing")
    for dest in range(4):
        self.distance_table[self.id][dest] = self.costs[dest]
    self.printdt()
    self.send_update()

def common_update(self, packet):
    """
    Process incoming routing info to see if we have a better route.

    For each destination, checks whether the path through the source provides
    a lower cost. If any improvements are made, updates the table and sends
    the new minimum cost vector to neighbors.

    Args:
        packet: The distance vector packet received from a neighbor.
    """
    updated = False
    src = packet.src
    print(f"node {self.id} update from {src} received")

    for dest in range(4):
        via_src_cost = self.costs[src] + packet.mincost[dest]
        if via_src_cost < self.distance_table[self.id][dest]:
            self.distance_table[self.id][dest] = via_src_cost
            updated = True
            print(f"  updated path to {dest} via {src} with cost {via_src_cost}")

        if packet.mincost[dest] < self.distance_table[src][dest]:
            self.distance_table[src][dest] = packet.mincost[dest]  # optional backup info

    if updated:
        print("  changes based on update")
        self.printdt()
        self.send_update()
    else:
        print(f"  no changes in node {self.id}, so nothing to do")
        self.printdt()

def common_link_cost_change(self, to_entity, new_cost):
    """
    React to changes in the network — like a neighbor getting closer or farther.

    Updates the cost in the distance table and sends a new distance vector 
    if the change could affect routing decisions.

    Args:
        to_entity (int): ID of the neighbor whose link cost changed.
        new_cost (int): New cost of the link to that neighbor.
    """
    print(f"node {self.id}: link cost change to {to_entity} from {self.costs[to_entity]} to {new_cost}")
    self.costs[to_entity] = new_cost
    self.distance_table[self.id][to_entity] = new_cost
    self.send_update()

# ========== Entity Definitions ==========

class Entity0(Entity):
    """
    Entity 0's view of the network and how it talks to neighbors.

    Initializes node ID, costs to neighbors, and triggers distance vector initialization.
    Handles update and link cost change events using shared logic functions.
    """
    def __init__(self):
        self.id = 0
        self.costs = [0, 1, 3, 7]
        self.neighbors = [1, 2, 3]
        common_init(self)

    def update(self, packet):
        """
        Delegates to shared logic to determine whether the table should be updated
        and whether an updated vector should be sent to neighbors.

        Args:
        packet: A distance vector received from a neighbor.
        """
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        """
        Adjust our routing when a neighbors cost changes.

        Updates internal state and recomputes the node's view of minimum costs.

        Args:
        to_entity (int): ID of the neighbor with changed link cost.
        new_cost (int): New cost to reach that neighbor.
        """
        common_link_cost_change(self, to_entity, new_cost)

    def send_update(self):
        """
        Share latest best guesses with the rest.

        Extracts the current shortest known cost to each destination and uses
        to_layer_2() to send this vector to each neighbor.
        """
        mincost = self.distance_table[self.id][:]
        print(f"sending mincost updates to neighbors")
        for neighbor in self.neighbors:
            to_layer_2(self.id, neighbor, mincost)

    def printdt(self):
        """
        Snapshot our routing table to see how were doing.

        Outputs the entire table row-by-row with the node ID for context.
        Used for visual verification of state during simulation.
        """
        print(f"node: {self.id}")
        for row in self.distance_table:
            print(row)

class Entity1(Entity):
    def __init__(self):
        self.id = 1
        self.costs = [1, 0, 1, float('inf')]
        self.neighbors = [0, 2]
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost)

    def send_update(self):
        mincost = self.distance_table[self.id][:]
        print(f"sending mincost updates to neighbors")
        for neighbor in self.neighbors:
            to_layer_2(self.id, neighbor, mincost)

    def printdt(self):
        print(f"node: {self.id}")
        for row in self.distance_table:
            print(row)

class Entity2(Entity):
    def __init__(self):
        self.id = 2
        self.costs = [3, 1, 0, 2]
        self.neighbors = [0, 1, 3]
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost)

    def send_update(self):
        mincost = self.distance_table[self.id][:]
        print(f"sending mincost updates to neighbors")
        for neighbor in self.neighbors:
            to_layer_2(self.id, neighbor, mincost)

    def printdt(self):
        print(f"node: {self.id}")
        for row in self.distance_table:
            print(row)

class Entity3(Entity):
    def __init__(self):
        self.id = 3
        self.costs = [7, float('inf'), 2, 0]
        self.neighbors = [0, 2]
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost)

    def send_update(self):
        mincost = self.distance_table[self.id][:]
        print(f"sending mincost updates to neighbors")
        for neighbor in self.neighbors:
            to_layer_2(self.id, neighbor, mincost)

    def printdt(self):
        print(f"node: {self.id}")
        for row in self.distance_table:
            print(row)

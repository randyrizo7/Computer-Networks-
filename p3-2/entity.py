"""
CPSC 5510, Seattle University, Project #3
Based on the Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""


class Entity(object):
    """Base class for student-supplied classes for each node
    DO NOT CHANGE ANYTHING IN THIS BASE CLASS
    """

    def __init__(self):
        """subclasses should invoke this parent class ctor:
        super().__init__()
        Students are not allowed to change this method here in the base class,
        but they may change the self values node and distance_table in their
        own __init__ and they may add additional instance data.
        """
        self.node = 0  # subclass should set this to 0, 1, 2, or 3
        self.distance_table = [[float('inf') for i in range(4)] for j in
                               range(4)]

    def __str__(self):
        """this should work for printing out one of the entities"""
        s = 'node: ' + str(self.node) + '\n'
        for row in self.distance_table:
            s += '{}\n'.format(row)
        return s

    def update(self, packet):
        raise NotImplemented('Student must implement this in the subclasses')

    def link_cost_change(self, to_entity, new_cost):
        raise NotImplemented('Student must implement this in the subclasses')

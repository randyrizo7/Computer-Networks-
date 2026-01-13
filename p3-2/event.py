"""
CPSC 5510, Seattle University, Project #3
Based on the Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""

FROM_LAYER_2 = 0
LINK_CHANGE = 1


class Event(object):

    def __init__(self, time, type, entity, packet=None):
        self.time = time
        self.type = type
        self.entity = entity
        self.packet = packet

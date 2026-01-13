"""
CPSC 5510, Seattle University, Project #3
Based on the Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""
import network_simulator


class Packet(object):
    def __init__(self, src, dest, mincost):
        if not self.valid(src) or not self.valid(dest):
            raise ValueError('Illegal entity for packet')
        self.src = src
        self.dest = dest
        self.mincost = mincost[:]

    def __str__(self):
        return 'src={}, dest={}, mincost={}'.format(self.src, self.dest,
                                                    self.mincost)

    @staticmethod
    def valid(entity):
        return entity in range(network_simulator.NUM_ENTITIES + 1)

"""
CPSC 5510, Seattle University, Project #3
Based on the Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""
import random

from event_list import *
from student_entities import *

INF = float('inf')
NUM_ENTITIES = 4


class NetworkSimulator(object):
    """simulator for the project--invoked from project.py"""

    event_list = EventList()
    cost = [[0, 1, 3, 7], [1, 0, 1, INF], [3, 1, 0, 2], [7, INF, 2, 0]]
    time = 0.0
    has_change = False
    trace = False

    @classmethod
    def run_simulator(cls, has_change, trace, seed):
        cls.has_change = has_change
        cls.trace = trace
        random.seed(seed)

        cls.time = 0.0
        print('\n\nSimulator started at t =', cls.time, '\n')
        cls.event_list = EventList()
        entities = [Entity0(), Entity1(), Entity2(), Entity3()]
        if has_change:
            NetworkSimulator.event_list.add(Event(10000.0, LINK_CHANGE, 0))
            NetworkSimulator.event_list.add(Event(20000.0, LINK_CHANGE, 0))

        while True:
            event = cls.event_list.remove_next()
            if event is None:
                break
            if cls.trace > 1:
                print()
                print('main(): event received. t=' + str(
                    event.time) + ', node=' + str(event.entity))
                if event.type == FROM_LAYER_2:
                    print(' ', event.packet)
                elif event.type == LINK_CHANGE:
                    print(' ', 'Link cost change.')

            cls.time = event.time

            if event.type == FROM_LAYER_2:
                p = event.packet
                if event.entity not in range(NUM_ENTITIES + 1):
                    print('main(): Panic. Unknown event entity.')
                else:
                    entities[event.entity].update(p)
            elif event.type == LINK_CHANGE:
                if cls.time < 10001.0:
                    cls.cost[0][1] = 20
                    cls.cost[1][0] = 20
                    entities[0].link_cost_change(1, 20)
                    entities[1].link_cost_change(0, 20)
                else:
                    cls.cost[0][1] = 1
                    cls.cost[1][0] = 1
                    entities[0].link_cost_change(1, 1)
                    entities[1].link_cost_change(0, 1)
            else:
                print('main(): Panic. Unknown event type.')
        print('Simulator terminated at t =', cls.time,
              '-- no packets in medium.')

    @classmethod
    def _to_layer_2(cls, p):
        """Students do not call this directly. Use to_layer_2 function from
        student_utilities module.
        """
        if p.src == p.dest:
            raise ValueError('packet has same src and dest')
        if cls.cost[p.src][p.dest] == INF:
            raise ValueError('src not connected to dest')
        if cls.trace > 2:
            print('to_layer_2():', p)
        arrival = cls.event_list.last_packet_time(p.src, p.dest)
        if arrival == 0.0:
            arrival = cls.time
        arrival += 1.0 + random.random() * 9.0
        if cls.trace > 2:
            print('to_layer_2(): Scheduling arrival of packet.')

        event = Event(arrival, FROM_LAYER_2, p.dest, p)
        cls.event_list.add(event)

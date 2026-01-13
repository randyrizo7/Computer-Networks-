"""
CPSC 5510, Seattle University, Project #3
Based on the Kurose/Ross lab 6
https://media.pearsoncmg.com/aw/aw_kurose_network_3/labs/lab6/lab6.html
:Author: Kevin Lundeen
:Version: s23
"""
from event import *


class EventList(object):

    def __init__(self):
        self.data = []

    def add(self, event):
        self.data.append(event)

    def last_packet_time(self, entity_from, entity_to):
        time = 0.0
        for event in self.data:
            if (
                    event.type == FROM_LAYER_2 and event.entity == entity_to
                    and event.packet.src == entity_from):
                time = event.time
        return time

    def remove_next(self):
        if len(self.data) == 0:
            return None
        first_index = 0
        first = self.data[first_index].time
        for i, event in enumerate(self.data):
            if event.time < first:
                first = event.time
                first_index = i
        next_event = self.data[first_index]
        self.data.pop(first_index)
        return next_event

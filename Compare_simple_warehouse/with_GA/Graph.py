#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 eelium <eelium@eez008>
#
# Distributed under terms of the MIT license.

"""
graph construction 
"""

from param import *


graph_nodes = dict()
R1 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
R2 = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
R3 = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
R4 = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']


P1 = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8']
P2 = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8']


class node(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


def generateGraphNodes():
    global graph_nodes
    global R1,  R2,  R3,  R4
    global P1,  P2

    for i, p in enumerate(R1):
        graph_nodes[p] = node(
            margin_left + i * 3 * L + L / 2, margin_top + L / 2)
    for i, p in enumerate(R2):
        graph_nodes[p] = node(
            margin_left + i * 3 * L + L / 2, margin_top + 5 * L + L / 2)
    for i, p in enumerate(R3):
        graph_nodes[p] = node(
            margin_left + i * 3 * L + L / 2, margin_top + 10 * L + L / 2)
    for i, p in enumerate(R4):
        graph_nodes[p] = node(
            margin_left + i * 3 * L + L / 2, margin_top + 15 * L + L / 2)

    for i, p in enumerate(P1):
        graph_nodes[p] = node(margin_left + i * 3 * L + L / 2, margin_top - 25)
        
    for i, p in enumerate(P2):
        graph_nodes[p] = node(
            margin_left + i * 3 * L + L / 2, world_height - margin_bottom + 25)
        
    return graph_nodes


def generateGraph():
    global R1,  R2,  R3,  R4
    # horizon
    # raw
    L1 = R1
    L2 = R2[::-1]  # reversed
    L3 = R3
    L4 = R4[::-1]  # reversed
    # vertical
    C1 = ['A1', 'B1', 'C1', 'D1']
    C2 = ['A2', 'B2', 'C2', 'D2']
    C3 = ['A3', 'B3', 'C3', 'D3']
    C4 = ['A4', 'B4', 'C4', 'D4']
    C5 = ['A5', 'B5', 'C5', 'D5']
    C6 = ['A6', 'B6', 'C6', 'D6']
    C7 = ['A7', 'B7', 'C7', 'D7']
    C8 = ['A8', 'B8', 'C8', 'D8']


    C1 = [k for k in C1[::-1]]
    C2 = [k for k in C2]
    C3 = [k for k in C3[::-1]]
    C4 = [k for k in C4]
    C5 = [k for k in C5[::-1]]
    C6 = [k for k in C6]
    C7 = [k for k in C7[::-1]]
    C8 = [k for k in C8]

    graph = {}
    for ns in [L1, L2, L3, L4,
               C1, C2, C3, C4, C5, C6, C7, C8]:
        for i, n in enumerate(ns):
            if graph.has_key(n):
                try:
                    graph[n].append(ns[i + 1])
                except IndexError:
                    pass
            else:
                graph[n] = []
                try:
                    graph[n].append(ns[i + 1])
                except IndexError:
                    pass

    # Add the path for parking
    graph['Y1'] = ['A1']
    graph['Y2'] = ['A2']
    graph['Y3'] = ['A3']
    graph['Y4'] = ['A4']
    graph['Y5'] = ['A5']
    graph['Y6'] = ['A6']
    graph['Y7'] = ['A7']
    graph['Y8'] = ['A8']

    graph['A1'].append('Y1')
    graph['A2'].append('Y2')
    graph['A3'].append('Y3')
    graph['A4'].append('Y4')
    graph['A5'].append('Y5')
    graph['A6'].append('Y6')
    graph['A7'].append('Y7')
    graph['A8'].append('Y8')

    graph['Z1'] = ['D1']
    graph['Z5'] = ['D5']
    
    graph['Z4'] = ['Z1']
    graph['Z8'] = ['Z5']
 
    graph['D4'].append('Z4')
    graph['D8'].append('Z8')

    return graph


class MyQUEUE:  # just an implementation of a queue

    def __init__(self):
        self.holder = []

    def enqueue(self, val):
        self.holder.append(val)

    def dequeue(self):
        val = None
        try:
            val = self.holder[0]
            if len(self.holder) == 1:
                self.holder = []
            else:
                self.holder = self.holder[1:]
        except:
            pass

        return val

    def IsEmpty(self):
        result = False
        if len(self.holder) == 0:
            result = True
        return result


# path_queue = MyQUEUE() # now we make a queue


def BFS(graph, start, end, q):
    cnts = 0
    temp_path = [start]
    q.enqueue(temp_path)

    while q.IsEmpty() == False:
        cnts += 1
#         print 'Path List:', q.holder
        tmp_path = q.dequeue()
        last_node = tmp_path[len(tmp_path) - 1]
#         print cnts, tmp_path
        if last_node == end:
            #         print "VALID_PATH : ", tmp_path
            #             raw_input('prompt')
            return tmp_path
        # need to reduce the search space
        # if distance_start_goal_x >= distance_start_goal_y along the x search
        for link_node in graph[last_node]:
            if abs(graph_nodes[link_node].x - graph_nodes[start].x) <= 150:
                if abs(graph_nodes[link_node].y - graph_nodes[end].y) - abs(graph_nodes[last_node].y - graph_nodes[end].y) <= 300:
                    if link_node not in tmp_path:
                        new_path = tmp_path + [link_node]
                        q.enqueue(new_path)
            elif abs(graph_nodes[link_node].y - graph_nodes[end].y) <= 300:
                if abs(graph_nodes[link_node].x - graph_nodes[end].x) - abs(graph_nodes[last_node].x - graph_nodes[end].x) <= 150:
                    if link_node not in tmp_path:
                        new_path = tmp_path + [link_node]
                        q.enqueue(new_path)

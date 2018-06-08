#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 eelium <eelium@eez008>
#
# Distributed under terms of the MIT license.
import random
"""
parameters 
"""
# The window refresh rate
REFRESH_INTERVAL = 50

# the ground size 
margin_left = 100
margin_right = 100
margin_top = 100
margin_bottom = 100
L = 50  # unit value in pixel; as scalar
# the window size
world_height = 16 * L + margin_top + margin_bottom
world_width = 22 * L + margin_left + margin_right
# robot numbers
NUM_AGENTS = 8
# agent speed
agent_speed = 40
# TODO: parameterize this magic number
TIME_RATE = 2
FRAME_PER_SECOND = 20.0
# # collision allows the angle
# th_close_angle = 45
all_finish_mark = 0


# good position letter (forward,backward)
ROW1_LEFT = [
    ('B1', 'A1') , ('A2', 'B2') , ('B3', 'A3') , ('A4', 'B4') , ('B5', 'A5') ,
    ('A6', 'B6') , ('B7', 'A7')  ]
ROW1_RIGHT = [    
    ('A2', 'B2') , ('B3', 'A3') , ('A4', 'B4') , ('B5', 'A5') ,
    ('A6', 'B6') , ('B7', 'A7') , ('A8', 'B8')]

ROW2_LEFT = [
    ('C1', 'B1') , ('B2', 'C2') , ('C3', 'B3') , ('B4', 'C4') , ('C5', 'B5') , 
    ('B6', 'C6') , ('C7', 'B7') ]
ROW2_RIGHT = [
    ('B2', 'C2') , ('C3', 'B3') , ('B4', 'C4') , ('C5', 'B5') , 
    ('B6', 'C6') , ('C7', 'B7') , ('B8', 'C8') ]

ROW3_LEFT = [
    ('D1', 'C1') , ('C2', 'D2') , ('D3', 'C3') , ('C4', 'D4') , ('D5', 'C5') , 
    ('C6', 'D6') , ('D7', 'C7') ]
ROW3_RIGHT = [
    ('C2', 'D2') , ('D3', 'C3') , ('C4', 'D4') , ('D5', 'C5') , 
    ('C6', 'D6') , ('D7', 'C7') , ('C8', 'D8') ]

# #Class goods
# CLASS_GOODS_DIC = {
#     0: [0, 1, 2, 3, 4, 5, 6, 7], 
#     1: [8, 9, 10, 11, 12, 13, 14, 15], 
#     2: [16, 17, 18, 19, 20, 21, 22, 23], 
#     3: [24, 25, 26, 27, 28, 29, 30, 31], 
#     4: [32, 33, 34, 35, 36, 37, 38, 39], 
#     5: [40, 41, 42, 43, 44, 45, 46, 47], 
#     6: [48, 49, 50, 51, 52, 53, 54, 55], 
#     7: [56, 57, 58, 59, 60, 61, 62, 63], 
#     8: [64, 65, 66, 67, 68, 69, 70, 71], 
#     9: [72, 73, 74, 75, 76, 77, 78, 79], 
#     10: [80, 81, 82, 83, 84, 85, 86, 87], 
#     11: [88, 89, 90, 91, 92, 93, 94, 95], 
#     12: [96, 97, 98, 99, 100, 101, 102, 103], 
#     13: [104, 105, 106, 107, 108, 109, 110, 111], 
#     14: [112, 113, 114, 115, 116, 117, 118, 119], 
#     15: [120, 121, 122, 123, 124, 125, 126, 127], 
#     16: [128, 129, 130, 131, 132, 133, 134, 135], 
#     17: [136, 137, 138, 139, 140, 141, 142, 143], 
#     18: [144, 145, 146, 147, 148, 149, 150, 151], 
#     19: [152, 153, 154, 155, 156, 157, 158, 159], 
#     20: [160, 161, 162, 163, 164, 165, 166, 167]}


# charging park
CHARGING_PARK = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8']

# order points
UNLOADING_POSITION = ['Z1', 'Z5']

#goods colour
SHELVES_COLOR = {0:'BLUE', 1:'SLATE BLUE', 2:'GREEN', 3:'SPRING GREEN', 4:'CYAN', 5:'NAVY',
               6:'STEEL BLUE', 7:'FOREST GREEN', 8:'SEA GREEN', 9:'SEA GREEN', 10:'MIDNIGHT BLUE',
               11:'DARK GREEN', 12:'DARK SLATE GREY', 13:'MEDIUM BLUE', 14:'SKY BLUE', 15:'LIME GREEN',
               16:'MEDIUM AQUAMARINE', 17:'CORNFLOWER BLUE', 18:'MEDIUM SEA GREEN', 19:'INDIAN RED', 20:'VIOLET',
               21:'DARK OLIVE GREEN'}



# goods = 0
# #total goods
# for i in xrange(ORDER_NUM):
#     goods += len(GOODS_ORDER[i])
# TOTAL_GOODS = goods

# goods order

# GOODS_ORDER = {0:[790, 160, 1210, 1010, 130, 220, 590, 980, 1400, 1020, 1040, 370],
#                1:[650, 1170, 950, 1100, 540, 1650, 60, 470, 1500, 210, 890, 830, 990]} #1

# GOODS_ORDER = {0:[1150, 1340, 350, 110, 600, 670, 120, 1160, 1490, 790, 730, 1540],
#                1:[1210, 520, 1050, 400, 1140, 190, 210, 90, 870, 1560, 1130, 1640, 690]} #2

# GOODS_ORDER = {0:[40, 860, 150, 400, 690, 1570, 1630, 760, 1370, 1420, 320, 230],
#                1:[480, 1670, 1320, 1430, 1300, 1610, 280, 570, 920, 530, 910, 200, 260]} #3

# GOODS_ORDER = {0:[140, 450, 1250, 1230, 150, 1350, 970, 350, 120, 1430, 1550, 300],
#                1:[1100, 570, 1640, 160, 1070, 790, 770, 130, 1010, 830, 90, 550, 890]} #4

GOODS_ORDER = {0:[950, 1130, 1510, 550, 1200, 890, 1370, 1240, 990, 450, 1170, 440],
               1:[1180, 1640, 1290, 60, 480, 230, 370, 140, 740, 1310, 1480, 150, 870]} #5

# # # goods order
# GOODS_ORDER = {0:[790, 160, 1210, 1010, 130],
#                1:[650, 1170, 950]}
#order number 
ORDER_NUM = len(GOODS_ORDER)
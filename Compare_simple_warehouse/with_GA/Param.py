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
# GA iteration
GA_iteration = 300
# agent speed
agent_speed = 40
# TODO: parameterize this magic number
TIME_RATE = 2
FRAME_PER_SECOND = 20.0

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

# goods order
# GOODS_ORDER = {0:[790, 160, 1210, 1010, 130, 220, 590, 980, 1400, 1020, 1040, 370],
#                1:[650, 1170, 950, 1100, 540, 1650, 60, 470, 1500, 210, 890, 830, 990]}#1

# GOODS_ORDER = {0:[1150, 1340, 350, 110, 600, 670, 120, 1160, 1490, 790, 730, 1540],
#                1:[1210, 520, 1050, 400, 1140, 190, 210, 90, 870, 1560, 1130, 1640, 690]} #2

# GOODS_ORDER = {0:[40, 860, 150, 400, 690, 1570, 1630, 760, 1370, 1420, 320, 230],
#                1:[480, 1670, 1320, 1430, 1300, 1610, 280, 570, 920, 530, 910, 200, 260]} #3

# GOODS_ORDER = {0:[140, 450, 1250, 1230, 150, 1350, 970, 350, 120, 1430, 1550, 300],
#                1:[1100, 570, 1640, 160, 1070, 790, 770, 130, 1010, 830, 90, 550, 890]} #4

GOODS_ORDER = {0:[950, 1130, 1510, 550, 1200, 890, 1370, 1240, 990, 450, 1170, 440],
               1:[1180, 1640, 1290, 60, 480, 230, 370, 140, 740, 1310, 1480, 150, 870]} #5
#order number 
ORDER_NUM = len(GOODS_ORDER)
# unloading  position
UNLOADING_POSITION = ['Z1', 'Z5']
# charging park
CHARGING_PARK = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8']
INIT_CHROMOSOME = [79, 16, 121, 101, 13, 22, 59, 98, 140, 102, 104, 37, 65, 117, 95, 110, 54, 165, 6, 47, 150, 21, 89, 83, 99]
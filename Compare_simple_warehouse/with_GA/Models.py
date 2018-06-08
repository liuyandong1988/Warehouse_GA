import math
import random
from param import *

class shelves():  # goods to be operated
    def __init__(self):
        self.status = 0  # 0: empty  1: ocuppied
        self.x = 0.0  # top left corner x,y
        self.y = 0.0
        self.agentx = 0.0  # agent carry shelves position
        self.agenty = 0.0
        self.shelf_id = 0
        self.shelf_find_letter = ''  # find the goods forward letter
        self.shelf_color = ''
        self.unloading_position = ''
        self.goods_class = []


class point():
    x = 0
    y = 0
    r = 0
    
class boxes():
    def __init__(self):
        self.box_x = 0
        self.box_y = 0
        self.boxes_num = 0
        self.box_color = []

class orderGoods():
    def __init__(self):
        self.order_id = 0
        self.order_class = []
        self.unloading_position = ''


class angle():
    theta = 0.0

    def __init__(self, theta=0.0):
        self.theta = theta

    def increase(self, delta):
        self.theta += delta
        while self.theta > 361:
            self.theta -= 360

    def decrease(self, delta):
        self.theta -= delta
        while self.theta < 0:
            self.theta += 360

    def cos(self):
        return math.cos(self.theta * math.pi / 180.0)

    def sin(self):
        return math.sin(self.theta * math.pi / 180.0)

    def tan(self):
        return math.tan(self.theta * math.pi / 180.0)

    def fromAtan(self, atanValue):
        return angle(math.atan(atanValue) / 180.0 * math.pi)


class agent():  # agent robot to operate

    def __init__(self):
        # 0: idle; 1: moving to good; 2: carrying good to goal, 3: not in task
        # (dead)
        self.status = 0
        self.color = 0
        self.x = 0.0
        self.y = 0.0
        self.r = 0.2
        self.angle = angle()
        self.agent_id = -1
        self.charging_position = ''  # charging position
        self.shelf_num = 0  # agents goal
#         self.goods_class = 0
        # moving
        self.stop_mark = 0  # agents collision mark
        self.move_mark = 0
        self.return_mark = 0
        self.speed = agent_speed
        # good path forwardletter and backwardletter mark
        self.goods_forward_letter = 0
        # if the robot is moving to an intemediate node, this is true
        self.next_intermediate_goal = ''
        self.with_step_plan = 0
        # pick up goods
        self.waiting = 0  # pick up or take off goods waiting time
        self.get_goods = 0 # mark get good or not
        self.arrive_withgoods_mark = 0  
        self.arrive_goods_position = 0
        # take off goods
        self.takeoff_mark = 0
        self.check_run_again_mark = 0
        # finish_mark
        self.finish_mark = 0
#         self.finish_back_mark = 0
        
        # battery
        self.last_angle = 0
        self.battery_status = 1
        self.battery_angle1 = angle()
        self.battery_angle2 = angle()
        self.battery_full_pos = 0
        self.battery_pos = 0
        self.width = 0

#         # box
#         self.box_num = 0
#         self.box_x = 0  # top left corner x,y
#         self.box_y = 0

        # charging
        self.current_energy = 10
        self.full_energy = 10
        self.charge_mark = 0
        self.need_charge_mark = 0
        self.back_home_mark = 0
        self.back_to_charge = 0
        self.first_time_mark = 0
        self.current_status = 0
        self.charge_times = 0
        self.charg_energy = 0
        self.full_energy_mark = 1
        self.end_letter = ''
#         self.last_letter = ''
        #consumption
        self.step_times = 0
        self.consume_energy = 0
        self.consume_mark = 0
        #record
        self.agent_start_mark = 0 
        self.agent_end_mark = 0
        self.agent_start_time = 0
        self.agent_end_time = 0
        self.work_time = 0
        # goods order
        self.order_id = 0
        self.shelf_on_agent = 0


        
    def move(self, offset):
        self.x += offset[0]
        self.y += offset[1]
        self.angle.theta = math.atan2(-offset[1], offset[0]) * 180 / math.pi

    def stepToGoal(self, goalCoor, step):  # nocheck on whether arrived
        offset = (0, 0)
        dy = goalCoor[1] - self.y
        dx = goalCoor[0] - self.x
        if dx == 0:
            # print "Easy dY [", self.agent_id, "]"
            if dy > 0:
                offset = (0, step)
            else:
                offset = (0, -step)
        if dy == 0:
            # print "Easy dX [", self.agent_id, "]"
            if dx > 0:
                offset = (step, 0)
            else:
                offset = (-step, 0)
        if (dx != 0) and (dy != 0):
            theta = math.atan2(-dy, dx)
            offset = (step * math.cos(theta), step * math.sin(theta))
        self.move(offset)

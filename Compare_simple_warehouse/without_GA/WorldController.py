import Models
from param import *
import Graph
import InitStartGoal
import Strategy
import math
import ChargeThreshold
import time
# import RecordData

start_time = 0
end_time = 0
run_time = 0
total_get_goods_number = 0
class Controller:

    def __init__(self):

#         self.goods_timestep_cnt = 0  # record the times
        self.collision_total_cnt = 0 # record the collisions
        self.collision_agents = []  # log the collision agents
        self.start_time_mark = 0
        self.stop_mark = 0
        self.start_time = 0

        
        # add shelves
        self.shelves = [Models.shelves() for i in xrange(21 * 8)]
        # put shelves in warehouse
        row1left = 0   # index the goods position  to mark letter
        row2left = 0
        row3left = 0
        row1right = 0
        row2right = 0
        row3right = 0
    
        for group in xrange(21):
            offset = (0, 0)
            if group % 3 == 0:  # row1
                offset = (
                    (3 * (group / 3) + 1) * L + margin_left, margin_top + L)
            elif group % 3 == 1:  # row2
                offset = (
                    (3 * (group / 3) + 1) * L + margin_left, margin_top + 6 * L)
            elif group % 3 == 2:  # row3
                offset = (
                    (3 * (group / 3) + 1) * L + margin_left, margin_top + 11 * L)

            # print "for good in group ", group, " Offset: ", offset
            for i in range(8):
                if (i % 2 == 0):  # on left
                    self.shelves[i + group * 8].id = i + group * 8 
                    self.shelves[i + group * 8].status = 1
                    # every shelf has 10 class goods   goods_class_index
                    for goods_type in xrange(self.shelves[i + group * 8].id * 10,self.shelves[i + group * 8].id * 10+10):
                        self.shelves[i + group * 8].goods_class.append(goods_type)
                    self.shelves[i + group * 8].shelf_color = 'red'
                    self.shelves[i + group * 8].x = offset[0]
                    self.shelves[i + group * 8].y = offset[1] + int(i / 2) * L
                    self.shelves[
                        i + group * 8].agentx = self.shelves[i + group * 8].x - 25
                    self.shelves[
                        i + group * 8].agenty = self.shelves[i + group * 8].y + 25

                    if group % 3 == 0:  # row1
                        self.shelves[
                            i + group * 8].shelf_find_letter = ROW1_LEFT[row1left]
                    elif group % 3 == 1:  # row2
                        self.shelves[
                            i + group * 8].shelf_find_letter = ROW2_LEFT[row2left]
                    elif group % 3 == 2:  # row3
                        self.shelves[
                            i + group * 8].shelf_find_letter = ROW3_LEFT[row3left]

                elif (i % 2 == 1):  # on right
                    self.shelves[i + group * 8].id = i + group * 8 
                    self.shelves[i + group * 8].status = 1
                    for goods_type in xrange(self.shelves[i + group * 8].id * 10,self.shelves[i + group * 8].id * 10+10):
                        self.shelves[i + group * 8].goods_class.append(goods_type)
                    self.shelves[i + group * 8].shelf_color = 'red'
                    self.shelves[i + group * 8].x = offset[0] + L
                    self.shelves[i + group * 8].y = offset[1] + int(i / 2) * L
                    self.shelves[
                        i + group * 8].agentx = self.shelves[i + group * 8].x + 75
                    self.shelves[
                        i + group * 8].agenty = self.shelves[i + group * 8].y + 25
                    if group % 3 == 0:  # row1
                        self.shelves[
                            i + group * 8].shelf_find_letter = ROW1_RIGHT[row1right]
                    elif group % 3 == 1:  # row2
                        self.shelves[
                            i + group * 8].shelf_find_letter = ROW2_RIGHT[row2right]
                    elif group % 3 == 2:  # row3
                        self.shelves[
                            i + group * 8].shelf_find_letter = ROW3_RIGHT[row3right]

            if group % 3 == 0:
                row1left += 1
                row1right += 1
            elif group % 3 == 1:
                row2left += 1
                row2right += 1
            elif group % 3 == 2:
                row3left += 1
                row3right += 1

        # generate graph
        self.graph_nodes = Graph.generateGraphNodes()
        self.graph = Graph.generateGraph()

        # the agent charging position and the box position
        self.chargePoints = [Models.point() for i in xrange(NUM_AGENTS)]

        agents_theta = -90
        battery_theta = agents_theta - 135
        # add agents
        self.agents = [Models.agent() for i in xrange(NUM_AGENTS)]
        for r in xrange(NUM_AGENTS):
            if r < NUM_AGENTS / 2:
                self.agents[r].x = world_width / 2 - r * L
            else:
                self.agents[r].x = world_width / 2 + r * L
            self.agents[r].y = L
            self.agents[r].r = L / 4
            self.agents[r].status = 3  # all dead
            self.agents[r].color = 3
            self.agents[r].angle = Models.angle(agents_theta)
            self.agents[r].last_angle = agents_theta
            self.agents[r].agent_id = r

            self.agents[r].battery_status = 1
            self.agents[r].battery_angle1 = Models.angle(battery_theta)
            self.agents[r].battery_angle2 = Models.angle(battery_theta - 90)

            self.chargePoints[r].x = Graph.graph_nodes[CHARGING_PARK[r]].x
            self.chargePoints[r].y = Graph.graph_nodes[CHARGING_PARK[r]].y
            self.chargePoints[r].r = L / 3

        # draw unloading mark 
        self.orderPoints = [Models.point() for i in xrange(ORDER_NUM)]
        for r in xrange(ORDER_NUM):            
            self.orderPoints[r].x = Graph.graph_nodes[UNLOADING_POSITION[r]].x
            self.orderPoints[r].y = Graph.graph_nodes[UNLOADING_POSITION[r]].y
            self.orderPoints[r].r = L / 3
            
        # draw the boxes
        self.orderBoxes = [Models.boxes() for i in xrange(ORDER_NUM)]
        for r in xrange(ORDER_NUM):
            offset = (self.orderPoints[r].x, self.orderPoints[r].y)
            self.orderBoxes[r].box_x = offset[0] 
            self.orderBoxes[r].box_y = offset[1] + L
            
        # initial order
        self.orderGoods = [Models.orderGoods() for i in xrange(ORDER_NUM)]
        for r in xrange(ORDER_NUM):
            self.orderGoods[r].order_id = r
            self.orderGoods[r].order_class = GOODS_ORDER[r]
            self.orderGoods[r].unloading_position = UNLOADING_POSITION[r] 

        # initial agents start and goal position letter task allocation
        self.initStartGoal = InitStartGoal.InitStartGoal(
            self.agents, self.shelves, self.orderGoods, self.graph_nodes, self.graph)
    
        # set the plan strategy
        self.strategy = Strategy.Strategy(
            self.shelves, self.agents, self.orderGoods,self.orderBoxes, self.graph_nodes, self.graph)
            
        # set agent charge
        self.agentCharge = ChargeThreshold.AgentCharge(
            self.agents, self.graph, self.shelves, self.graph_nodes, threshold_energy=3, consuming_rate=0.0001, charging_rate=0.05)
   
# #         # record the data
# #         self.recordData = RecordData.Record(self.agents)
         
    # check the collision needs the function
    # collision allow the angle
    def angle_is_close(self, a, b):
        return (abs(a - b) < 45)

    # collision distance
    def collisionBetweenAgents(self, a, b):
        if math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2) <= a.r + b.r + 23:
            return True
        return False

    # check the collision among the agents
    def checkCollisionsAndStop(self):
        for i in self.agents:
            for j in self.agents:
                if i == j:
                    continue
                else:
                    if self.collisionBetweenAgents(i, j):
                        angle_i_to_j = math.atan2(-(j.y - i.y),
                                                  j.x - i.x) * 180 / math.pi
                        # the special position collision
                        if (abs(angle_i_to_j - i.angle.theta) == 45 
                        or abs(angle_i_to_j - i.angle.theta) == 135):
                            if (i.agent_id, j.agent_id) not in self.collision_agents:
                                if j.stop_mark == 0:
                                    self.collision_agents.append(
                                        (i.agent_id, j.agent_id))
                                    i.stop_mark = 1
                        elif self.angle_is_close(angle_i_to_j, i.angle.theta):
                            if (i.agent_id, j.agent_id) not in self.collision_agents:
                                self.collision_agents.append(
                                    (i.agent_id, j.agent_id))
                                i.stop_mark = 1
                    else:
                        restore_mark = 0
                        # collision finish and run again
                        if len(self.collision_agents) != 0:
                            if (i.agent_id, j.agent_id) in self.collision_agents:
                                distance = math.sqrt(
                                    (i.x - j.x) ** 2 + (i.y - j.y) ** 2)
                                if distance > 60 and j.move_mark == 1 or j.charge_mark ==1:
                                    self.collision_agents.remove(
                                        (i.agent_id, j.agent_id))
                                    self.collision_total_cnt += 1
                                    for check_unit in self.collision_agents[:]:
                                        if i.agent_id == check_unit[0]:
                                            restore_mark = 1
                                            break
                                    if restore_mark == 0:
                                        i.stop_mark = 0


    # the agent life bar need change the angle
    def findAngle(self):
        for i in self.agents:
            if i.last_angle != i.angle.theta:
                i.last_angle = i.angle.theta - 135
                i.battery_angle1 = Models.angle(i.last_angle)
                i.battery_angle2 = Models.angle(i.last_angle - 90)
            else:
                pass
            if i.angle.theta == 90 or i.angle.theta == -90:
                i.battery_full_pos = i.x + 2 * i.r * i.battery_angle1.cos(
                ) - (i.x + 2 * i.r * i.battery_angle2.cos())
                i.width = (i.y + 3 * i.r * i.battery_angle2.cos() -
                    (i.y + 2 * i.r * i.battery_angle2.cos()))
            elif i.angle.theta == 0 or i.angle.theta == 180:
                i.battery_full_pos = (i.y - 2 * i.r * 
                    i.battery_angle1.sin() - 
                    (i.y - 2 * i.r * i.battery_angle2.sin()))
                i.width = (i.x + 2 * i.r * i.battery_angle1.cos() - 
                    (i.x + 3 * i.r * i.battery_angle1.cos()))

    #  show the power based on the proportion
    def batteryShow(self):
        for r in self.agents:
            if r.current_energy >= 0.8 * r.full_energy:
                r.battery_pos = r.battery_full_pos
                r.battery_status = 1  # green
            elif r.current_energy >= 0.6 * r.full_energy:
                r.battery_pos = r.battery_full_pos * 0.8
                r.battery_status = 1  # green
            elif r.current_energy >= 0.4 * r.full_energy:
                r.battery_pos = r.battery_full_pos * 0.6
                r.battery_status = 2  # orange
            elif r.current_energy >= 0.2 * r.full_energy:
                r.battery_pos = r.battery_full_pos * 0.4
                r.battery_status = 2  # orange
            else:
                r.battery_pos = r.battery_full_pos * 0.2
                r.battery_status = 3  # red

    # charge control
    def chargeController(self):
        for r in self.agents:
            # consume or charge mark
            if r.charge_mark == 1:
                # begin charging
                r.stop_mark = 1
                r.consume_mark = 0
                self.agentCharge.charging(r.agent_id)
                # full Electricity mark and waitting to fetch goods again
                if r.full_energy_mark == 1:
                        # reset the move forward mark
                        r.color = 0
                        r.with_step_plan = 0
                        r.back_home_mark = 0
                        r.step_times = 0
                        r.charge_times = 0
                        r.charge_mark = 0
                        r.first_time_mark = 0 #first time know needs to charge
                        r.back_to_charge = 0
                        r.need_charge_mark = 0
                        r.goods_forward_letter = 0
                        r.arrive_withgoods_mark = 0
                        r.arrive_without_goods_mark = 0
                        r.return_mark = 0
                        goal_letter = ''
                        if goal_letter == '': 
                            r.finish_mark = 1
                        else:                  
                            self.strategy.setNewPlan(r.agent_id, r.charging_position, goal_letter)
                            print 'Finish charging and fetch again !'
                            r.with_step_plan = 0
                            r.full_energy_mark = 0
                            r.check_run_again_mark = 1
            else:
                # Electricity consuming
                self.agentCharge.eleconsume(r.agent_id)
                
    # the working time is over and stop the working agents
    def timerController(self):
        cnt = 0
        makespan = 0
        if self.start_time_mark == 0:
            self.start_time = time.time()
            self.start_time_mark = 1
        for i in self.agents:
            if i.finish_mark == 1:
                cnt +=1
            if cnt == NUM_AGENTS and self.stop_mark == 0 :
                end_time = time.time() 
                print end_time,start_time
                makespan = end_time - self.start_time 
                self.stop_mark = 1
                print 'Makespan:', makespan
                print 'Task allocation:', InitStartGoal.task_allocation_record
                print 'Each agent distance:',InitStartGoal.each_agent_distance
                print 'The total distance:',InitStartGoal.distance_total
                

    def update(self):
        global total_get_goods_number
        # TODO avoid collision among agents
        self.checkCollisionsAndStop()
        # agents fetch goods
        self.strategy.computeStartToGood()
        # calculate the energy consume
        self.chargeController()
        # battery bar angle
        self.findAngle()
        # show the battery
        self.batteryShow()
        # start and stop timer
        self.timerController()

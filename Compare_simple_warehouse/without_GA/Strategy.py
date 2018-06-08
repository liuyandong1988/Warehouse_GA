import math
import random
from Graph import MyQUEUE, BFS
from param import *
import InitStartGoal

class Strategy():

    def __init__(self, shelves, agents, orderGoods ,orderBoxes, graph_nodes, graph):

        self.shelves = shelves
        self.agents = agents
        self.orderGoods = orderGoods
        self.orderBoxes = orderBoxes
        self.graph_nodes = graph_nodes
        self.graph = graph
        self.path_queues = [MyQUEUE() for i in xrange(NUM_AGENTS)]
        self.current_overall_plans = {}  # agent_id overall plans
        self.active_agents = []  # a list of ids of active (not dead) agents

        # put agent to corresponding letter position
        for i in self.agents:
            i.color = 0
            self.dummyTeleporterToNode(
                i.agent_id, i.charging_position, -90)
  
        # agent_id & goal
        for i in self.agents:
            if i.status == 0:
                i.status = 1
                i.color = 1
                i.stop_mark = 0
                i.consume_mark = 1
                i.full_energy_mark = 0
                self.setNewPlan(
                    i.agent_id, i.charging_position, self.shelves[i.shelf_num].shelf_find_letter[0])
               
    # put the agent to an accurate position
    def dummyTeleporterToNode(self, agent_id, letter, angle):
        self.dummyTeleporter(
            agent_id, (self.graph_nodes[letter].x, self.graph_nodes[letter].y), angle)

    def dummyTeleporter(self, agent_id, toWhere, angle):
        self.agents[agent_id].x, self.agents[agent_id].y = toWhere
        self.agents[agent_id].angle.theta = angle
        # change the dead agent to idle status and anothers do not
        if self.agents[agent_id].status == 3:
            self.agents[agent_id].status = 0

    # set a new plan from start letter to goalletter
    def setNewPlan(self, agent_id, start, goal_letter):
        self.current_overall_plans[agent_id] = BFS(
            self.graph, start, goal_letter, self.path_queues[agent_id])  # find the path to goal
        self.agents[agent_id].end_letter = self.current_overall_plans[agent_id][-1]
        print 'Agent %d: %s' % (agent_id, self.current_overall_plans[agent_id])

    # get the next letter on the path
    def getNextPlannedNode(self, agent_id):
        if not self.current_overall_plans.has_key(agent_id):
            #print "no plan for agent ", agent_id
            return 'x'
        elif self.current_overall_plans[agent_id] == []:  # all plans are done
            return 'x'
        else:  # with valid plan (normal case)
            plan = self.current_overall_plans[agent_id][0]
            return plan

    # go to the letter position
    def travelToNextNode(self, agent_id):
        if (self.agents[agent_id].need_charge_mark == 0 and self.agents[agent_id].back_home_mark == 0 
            and self.agents[agent_id].status != 2) :
            self.agents[agent_id].color = 1  #different from return to charge and color blink
        if self.agents[agent_id].next_intermediate_goal == 'x':
            return
        nextgoalletter_x = self.graph_nodes[
            self.agents[agent_id].next_intermediate_goal].x
        nextgoalletter_y = self.graph_nodes[
            self.agents[agent_id].next_intermediate_goal].y
        goal = (nextgoalletter_x, nextgoalletter_y)
        step = (TIME_RATE / FRAME_PER_SECOND) * self.agents[agent_id].speed
        distance = math.sqrt(
            (self.agents[agent_id].x - goal[0])**2 + (self.agents[agent_id].y - goal[1])**2)
        # agent with goods set the new plan with goods
        if distance < 5.0:
            # from the goods position to backward letter position
            if self.agents[agent_id].arrive_withgoods_mark == 1:
                goods_back_letter = self.agents[agent_id].next_intermediate_goal
                out_letter = self.shelves[self.agents[agent_id].shelf_num].unloading_position
                self.agents[agent_id].arrive_withgoods_mark = 0
                self.path_queues[agent_id].holder = []
                self.setNewPlan(agent_id, goods_back_letter, out_letter)
                print 'Agent fetches the goods and moves to unload !'
            else:
                self.current_overall_plans[agent_id].pop(0)
            self.agents[agent_id].with_step_plan = 0
            self.dummyTeleporterToNode(
                agent_id, self.agents[agent_id].next_intermediate_goal, self.agents[agent_id].angle.theta)  # hard reset to position
            return
        if step > distance:  # too fast
            self.agents[agent_id].stepToGoal(goal, distance)
        else:
            self.agents[agent_id].stepToGoal(goal, step)

    # go to the good position
    def travelTogoods(self, agent_id, agent_position):
        distance = math.sqrt(
            (self.agents[agent_id].x - agent_position[0])**2 + (self.agents[agent_id].y - agent_position[1])**2)
        step = (TIME_RATE / FRAME_PER_SECOND) * self.agents[agent_id].speed
        if distance < 5.0:
            # leave the letter forward letter
            self.agents[agent_id].goods_forward_letter = 0
            # change agent statues ready to get goods
            self.agents[agent_id].arrive_goods_position = 1
        if step > distance:  # too fast
            self.agents[agent_id].stepToGoal(agent_position, distance)
        else:
            self.agents[agent_id].stepToGoal(agent_position, step)

    # pick up the goods
    def pickupGoods(self, agent_id):
        if self.agents[agent_id].get_goods == 0:  # mark get good or not
            # arrived goods waiting for picking up goods
            self.agents[agent_id].waiting += 1
            if self.agents[agent_id].waiting == 20:
                self.agents[agent_id].arrive_goods_position = 0
                self.agents[agent_id].waiting = 0
                # the different from arrive_without_goods_mark
                self.agents[agent_id].arrive_withgoods_mark = 1
                self.agents[agent_id].get_goods = 1
                self.agents[agent_id].status = 2
                self.agents[agent_id].color = 2
                self.agents[agent_id].shelf_on_agent = 1
                shelf_num = self.agents[agent_id].shelf_num 
                # get goods mark
                for index,pos in enumerate(UNLOADING_POSITION):
                    if self.shelves[self.agents[agent_id].shelf_num].unloading_position == pos:
                        self.orderBoxes[index].box_color.append(self.shelves[shelf_num].shelf_color) 
                self.agents[agent_id].next_intermediate_goal = self.shelves[shelf_num].shelf_find_letter[1]  # goods position to next letter
                self.shelves[shelf_num].status = 0
                self.shelves[shelf_num].shelf_color = 'BLACK'
                self.agents[agent_id].with_step_plan = 1

    # take off goods
    def takeoffGoods(self, agent_id):
        if self.agents[agent_id].get_goods == 1:
            # the agents position
            self.agents[agent_id].angle.theta = -90.0
            # arrived goods waiting for picking up goods
            self.agents[agent_id].waiting += 1
            if self.agents[agent_id].waiting == 20:
#                 self.total_getshelf_num += 1 # the total fetching goods
                self.agents[agent_id].takeoff_mark = 0
                # mark reset for next good
                self.agents[agent_id].waiting = 0
                self.agents[agent_id].get_goods = 0
                self.agents[agent_id].status = 2
                self.agents[agent_id].color = 5
                self.path_queues[agent_id].holder = []
                for index,pos in enumerate(UNLOADING_POSITION):
                    if self.shelves[self.agents[agent_id].shelf_num].unloading_position == pos:
                        self.orderBoxes[index].boxes_num += 1
#                         print index, self.orderBoxes[index].boxes_num
                        start_letter = self.shelves[self.agents[agent_id].shelf_num].unloading_position
                goal_letter = self.shelves[self.agents[agent_id].shelf_num].shelf_find_letter[0]
                self.setNewPlan(agent_id, start_letter, goal_letter)
                self.agents[agent_id].with_step_plan = 0
                self.agents[agent_id].check_run_again_mark = 1
                print 'Unload goods and fetch again !'  

    # take off shelf
    def takeoffShelf(self, agent_id):
        if self.agents[agent_id].shelf_on_agent == 1:
            self.agents[agent_id].waiting += 1
            if self.agents[agent_id].waiting == 20:
                # mark reset for next good
                self.agents[agent_id].waiting = 0
                self.agents[agent_id].shelf_on_agent = 0
                self.agents[agent_id].arrive_goods_position = 0
                self.agents[agent_id].status = 0
                self.agents[agent_id].color = 0
                shelf_num =self.agents[agent_id].shelf_num
                self.shelves[shelf_num].status = 1
                self.shelves[shelf_num].shelf_color = 'Red'
                self.path_queues[agent_id].holder = []
                start_letter = self.shelves[shelf_num].shelf_find_letter[1]
                self.agents[agent_id].next_intermediate_goal = start_letter
                if self.agents[agent_id].need_charge_mark == 1:
                    self.agents[agent_id].back_home_mark = 1
                    self.agents[agent_id].status = 1
                    self.agents[agent_id].color = 1     
                    print 'Out of power and return home!'               
                # Or continue loading without charging
                else:
                    shelf_num = self.agents[agent_id].shelf_num
                    start_letter = self.shelves[shelf_num].shelf_find_letter[1]
                    if InitStartGoal.task_allocation[agent_id]: 
                        self.agents[agent_id].shelf_num = InitStartGoal.task_allocation [agent_id][0]
                        shelf_num = self.agents[agent_id].shelf_num
                        InitStartGoal.task_allocation [agent_id].pop(0)
                        goal_letter =  self.shelves[shelf_num].shelf_find_letter[0]
                    else:
                        goal_letter = ''
                    if goal_letter != '':                    
                        self.setNewPlan(agent_id, start_letter, goal_letter)
                        print 'Loading next goods!'
                    else:
                        # the order is empty
                        self.agents[agent_id].back_home_mark = 1
                        self.agents[agent_id].stop_mark = 0
                        self.agents[agent_id].consume_mark = 1 
                        print 'Finish order and return home!'  
    
                self.agents[agent_id].with_step_plan = 1
         
    


    # charging
    def agentCharging(self, agent_id):
        self.agents[agent_id].status = 0
        self.dummyTeleporterToNode(
            agent_id, self.agents[agent_id].charging_position, -90)
        self.path_queues[agent_id].holder = []
        
    def checkRunAgain(self,agent_id):
#         if self.agents[agent_id].finish_mark == 1 :
#             self.agents[agent_id].charge_mark = 1
#             return
        for i in self.agents:
            if i.agent_id == agent_id:
                continue
            else:
                distance = math.sqrt((i.x - self.agents[agent_id].x) ** 2 + (i.y - self.agents[agent_id].y) ** 2) 
                angle = i.angle.theta - math.atan2(-(self.agents[agent_id].y - i.y),self.agents[agent_id].x - i.x) * 180 / math.pi
                # above and below row need different angle  
                if distance < 250 and angle== 0 and i.y !=self.agents[agent_id].y:
                    return
                if angle != 0 and i.y !=self.agents[agent_id].y:
                    if distance < 100:
                        return
        self.agents[agent_id].check_run_again_mark = 0

#     # finish working and parking
    def agentBackHome(self, agent_id):  
        self.agents[agent_id].return_mark = 1
        self.agents[agent_id].back_to_charge = 1
        self.path_queues[agent_id].holder = []
        self.setNewPlan(
            agent_id, self.agents[agent_id].next_intermediate_goal, self.agents[agent_id].charging_position)
        self.agents[agent_id].with_step_plan = 0
        print 'Return to home and charge !'

    # run plan to fetch goods
    def computeStartToGood(self):
        global goods_current_cnt
        for r in self.agents:
            # agent collision mark
            if r.stop_mark == 0 and r.consume_mark == 1:
                plan = ''
                if r.status == 3:  # agent dead statues
                    continue
                # check run again avoid head-to-head collisions
                elif r.check_run_again_mark == 1:
                    r.move_mark = 0
                    self.checkRunAgain(r.agent_id)
                # move agent from good forward letter to good
                elif r.goods_forward_letter == 1:
                    r.move_mark = 1
                    self.travelTogoods(r.agent_id, (self.shelves[r.shelf_num].agentx, self.shelves[
                        r.shelf_num].agenty))  # from forward letter to goods
#                # arrived at goods: in the goods_current_list or not
                elif r.arrive_goods_position == 1:
                    r.move_mark = 0
                    if r.shelf_on_agent == 0:
                        self.pickupGoods(r.agent_id)  # pick up goods
                    else:
                        self.takeoffShelf(r.agent_id) # take off shelf
                # arrived at unloading
                elif r.takeoff_mark == 1:
                    r.move_mark = 0
                    self.takeoffGoods(r.agent_id)  # take off goods

                # run among the letters
                else:
                    self.active_agents.append(r.agent_id)
                    # get the next node of  a seq of letter on the path
                    plan = self.getNextPlannedNode(r.agent_id)
                    # back_to_charge: charging back && back_home_mark: working time is over
                    # need to charge condition avoid the bug
                    if r.back_home_mark == 1 and r.return_mark == 0 :
                        self.agentBackHome(r.agent_id)
                    else:
                        if ( r.need_charge_mark == 1 and r.back_to_charge == 0
                             and r.back_home_mark == 0 ):
                            # without good
                            if r.current_status == 1:
                                print "Needs to charing! Plan the returning path!"
                                #insert goods number and goods class
#                                 GOODS_ORDER[r.order_id].insert(0,r.goods_class)
#                                 CLASS_GOODS_DIC[r.goods_class].insert(0,r.shelf_num)
#                                 print r.order_id,GOODS_ORDER[r.order_id]
#                                 print r.goods_class,CLASS_GOODS_DIC[r.goods_class]
                                # planning the charging path
                                self.path_queues[
                                        r.agent_id].holder = []
                                if plan == 'x':
                                    self.setNewPlan(
                                        r.agent_id, r.end_letter, r.charging_position) # 'x'Bug
                                else:
                                    self.setNewPlan(
                                        r.agent_id, plan, r.charging_position)
                                print 'Power off and return to charge !'
                                # mark go back to charge
                                r.back_to_charge = 1
                                r.with_step_plan = 1
                                r.next_intermediate_goal = plan
                        if r.with_step_plan:
                            r.move_mark = 1
                            self.travelToNextNode(r.agent_id)
                        else:
                            if (plan == 'x'):
                                # Back to charge
                                if r.back_to_charge == 1:
                                    r.charge_mark = 1
                                    r.need_charge_mark = 0
                                    self.agentCharging(r.agent_id)
                                elif r.get_goods == 1:
                                    # arrived at out take off goods
                                    r.takeoff_mark = 1                                    
                                elif r.goods_forward_letter == 0 :
                                    # arrived at good forward letter final
                                    r.goods_forward_letter = 1
                                else:
                                    pass
            #                         print "Continue ", r.agent_id, " to ", plan
                            r.next_intermediate_goal = plan
                            r.with_step_plan = 1

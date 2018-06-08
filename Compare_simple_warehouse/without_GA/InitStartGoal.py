from param import *
import random
from Graph import MyQUEUE, BFS
import copy

task_allocation_record = {}
task_allocation = {}
each_agent_distance = {}
distance_total = 0

class InitStartGoal():

    def __init__(self, agents, shelves, orderGoods, graph_nodes, graph):

        self.agents = agents
        self.shelves = shelves
        self.orderGoods = orderGoods
        self.graph = graph
        self.graph_nodes = graph_nodes
        self.path_que = [MyQUEUE() for i in xrange(NUM_AGENTS)]
        self.current_overall_paths = {}  # agent_id overall plans
        self.initStartgoal()
        self.initAgentsTasks()
        self.eachAgentTask()

    def initStartgoal(self):
        # charging position
        p = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8']
        for i in self.agents:  # give the agents start and goal letter
            i.charging_position = p[0]
            p.pop(0)

    # set a new plan from start letter to goalletter
    def setNewPlan(self, agent_id, start, goal_letter):
        self.current_overall_paths[agent_id] = BFS(
            self.graph, start, goal_letter, self.path_que[agent_id])  # find the path to goal
        path = self.current_overall_paths[agent_id]
        distance = 0 # calculate the path distance
        for i in xrange(len(path)):
            if i != len(path) - 1:
                if self.graph_nodes[path[i]].x == self.graph_nodes[path[i+1]].x:
                    distance += abs(self.graph_nodes[path[i]].y - self.graph_nodes[path[i+1]].y)
                else:
                    distance += abs(self.graph_nodes[path[i]].x - self.graph_nodes[path[i+1]].x)
#         print 'Agent %d: %s' % (agent_id, self.current_overall_plans[agent_id]),'Distance:', distance
        return distance
          
    def calDistance(self,agent_id,tasks):
        distances = 0
        last_task = 0
#         for index,task in enumerate(tasks):
#             #from the start to shelf
#             start = self.agents[agent_id].charging_position
#             goal = self.shelves[task].shelf_find_letter[0]
#             self.path_que[agent_id].holder = []
#             distances += self.setNewPlan(agent_id, start, goal)
#             # from the shelf to unloading position
#             start = self.shelves[task].shelf_find_letter[1]
#             goal = self.shelves[task].unloading_position 
#             self.path_que[agent_id].holder = []
#             distances += self.setNewPlan(agent_id, start, goal)
#             # from unloading position to shelf
#             start = self.shelves[task].unloading_position
#             goal = self.shelves[task].shelf_find_letter[0]
#             self.path_que[agent_id].holder = []
#             distances += self.setNewPlan(agent_id, start, goal)
#             start = self.shelves[task].shelf_find_letter[1]
#             goal = self.agents[agent_id].charging_position
#             self.path_que[agent_id].holder = []
#             distances += self.setNewPlan(agent_id, start, goal)
#             return distances
             
        for index,task in enumerate(tasks):
            if index == 0:
#                 print '-'*10
#                 print 'Calculate the first task distance!'
                # the first task
                #from the start to shelf
                start = self.agents[agent_id].charging_position
                goal = self.shelves[task].shelf_find_letter[0]
                self.path_que[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from the shelf to unloading position
                start = self.shelves[task].shelf_find_letter[1]
                goal = self.shelves[task].unloading_position 
                self.path_que[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from unloading position to shelf
                start = self.shelves[task].unloading_position
                goal = self.shelves[task].shelf_find_letter[0]
                self.path_que[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
          
            else:
#                 print '-'*10
#                 print 'Calculate the task distance!'
                # from the last task position to next task position
                start = self.shelves[last_task].shelf_find_letter[1]
                goal = self.shelves[task].shelf_find_letter[0] 
                self.path_que[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from the task position to unloading
                start = self.shelves[task].shelf_find_letter[1]
                goal = self.shelves[task].unloading_position 
                self.path_que[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from the unloading to shelf 
                start = self.shelves[task].unloading_position
                goal = self.shelves[task].shelf_find_letter[0]
                self.path_que[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                if index == len(tasks) - 1:
#                     print 'Calculate the return distance!'
                # the last task
                    start = self.shelves[task].shelf_find_letter[1]
                    goal = self.agents[agent_id].charging_position
                    self.path_que[agent_id].holder = []
                    distances += self.setNewPlan(agent_id, start, goal)
                    return distances
#                     print distances
#                     raw_input('prompt')
            last_task = task      
        
        
    def initAgentsTasks(self):
        global task_allocation_record, task_allocation, each_agent_distance, distance_total 
        total_task = []
        tmp = []
        for order_id in xrange(len(GOODS_ORDER)):    
            for goods_class in GOODS_ORDER[order_id]:
                self.shelves[int(goods_class/10)].in_order = order_id 
                self.shelves[int(goods_class/10)].unloading_position = self.orderGoods[order_id].unloading_position
            tmp = tmp + GOODS_ORDER[order_id] 
        for task in tmp:
            total_task.append(int(task/10))
        task_allocation = {0:total_task[0:3],1:total_task[3:6],2:total_task[6:9],3:total_task[9:12],4:total_task[12:15],5:total_task[15:18],6:total_task[18:21],7:total_task[21:]}
#         task_allocation = {0:[total_task[0]],1:[total_task[1]],2:[total_task[2]],3:[total_task[3]],4:[total_task[4]],5:[total_task[5]],6:[total_task[6]],7:[total_task[7]]}
        task_allocation_record = copy.deepcopy(task_allocation) 
        for agent_id,tasks in task_allocation.items():
            each_agent_distance[agent_id] = self.calDistance(agent_id,tasks)
            distance_total += each_agent_distance[agent_id]
        print 'Task allocation:',task_allocation,'Distance:', distance_total
        
    def eachAgentTask(self):
        global task_allocation
        for i in self.agents:
            i.shelf_num = task_allocation[i.agent_id][0]
            task_allocation[i.agent_id].pop(0)
            
   
                
            
            

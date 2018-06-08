from Param import *
import random
from Graph import MyQUEUE, BFS
from GA import GA 
import copy 

task_allocation = {}
task_allocation_record = {}
each_agent_distance = {}
distance_total = 0
best_chromosome = []

class GA_task_allocate():

    def __init__(self, agents, shelves, orderGoods, graph_nodes, graph):

        self.agents = agents
        self.shelves = shelves
        self.orderGoods = orderGoods
        self.graph = graph
        self.graph_nodes = graph_nodes
        self.path_queues = [MyQUEUE() for i in xrange(NUM_AGENTS)]
        self.current_overall_plans = {}  # agent_id overall plans
        self.initStartgoal()
        self.population_size = 100
        self.task_chromosome = []   
               
        for order_id in xrange(ORDER_NUM):    
            for goods_class in GOODS_ORDER[order_id]:
                self.shelves[int(goods_class/10)].in_order = order_id 
                self.shelves[int(goods_class/10)].unloading_position = UNLOADING_POSITION[order_id]
                self.task_chromosome =  self.task_chromosome +[int(goods_class/10)]
#         print self.task_chromosome
#         raw_input('prompt') 
        # instance the GA class
        self.ga = GA(cross_rate = 0.7, 
              mutation_rate = 0.02,
              population_size = self.population_size, 
              init_chromosome = self.task_chromosome,
              chromosome_length = len(self.task_chromosome),
              fitness_Fun = self.fitnessFun())
        self.GA_run(GA_iteration)
        self.eachAgentTask()

    def initStartgoal(self):
        # charging position
        p = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8']
        for i in self.agents:  # give the agents start and goal letter
            i.charging_position = p[0]
            p.pop(0)

    # set a new plan from start letter to goalletter
    def setNewPlan(self, agent_id, start, goal_letter):
        self.current_overall_plans[agent_id] = BFS(
            self.graph, start, goal_letter, self.path_queues[agent_id])  # find the path to goal
        path = self.current_overall_plans[agent_id]
        distance = 0
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
        for index,task in enumerate(tasks):
            if index == 0:
#                 print '-'*10
#                 print 'Calculate the first task distance!'
                # the first task
                #from the start to shelf
                start = self.agents[agent_id].charging_position
                goal = self.shelves[task].shelf_find_letter[0]
                self.path_queues[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from the shelf to unloading position
                start = self.shelves[task].shelf_find_letter[1]
                goal = self.shelves[task].unloading_position 
                self.path_queues[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from unloading position to shelf
                start = self.shelves[task].unloading_position
                goal = self.shelves[task].shelf_find_letter[0]
                self.path_queues[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
         
            else:
#                 print '-'*10
#                 print 'Calculate the task distance!'
                # from the last task position to next task position
                start = self.shelves[last_task].shelf_find_letter[1]
                goal = self.shelves[task].shelf_find_letter[0] 
                self.path_queues[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from the task position to unloading
                start = self.shelves[task].shelf_find_letter[1]
                goal = self.shelves[task].unloading_position 
                self.path_queues[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                # from the unloading to shelf 
                start = self.shelves[task].unloading_position
                goal = self.shelves[task].shelf_find_letter[0]
                self.path_queues[agent_id].holder = []
                distances += self.setNewPlan(agent_id, start, goal)
                if index == len(tasks) - 1:
#                     print 'Calculate the return distance!'
                # the last task
                    start = self.shelves[task].shelf_find_letter[1]
                    goal = self.agents[agent_id].charging_position
                    self.path_queues[agent_id].holder = []
                    distances += self.setNewPlan(agent_id, start, goal)
                    return distances
#                     print distances
#                     raw_input('prompt')
            last_task = task

    #distance among the cities
    def distance(self, order):
        global each_agent_distance, task_allocation
        distance_total = 0
        task_allocation = {0:order[0:3],1:order[3:6],2:order[6:9],3:order[9:12],4:order[12:15],5:order[15:18],6:order[18:21],7:order[21:]}
#         print task_allocation
        for agent_id,tasks in task_allocation.items():
            each_agent_distance[agent_id] = self.calDistance(agent_id,tasks)
            distance_total += each_agent_distance[agent_id]
#         print 'Distances:',each_agent_distance,'Total distance:',distance_total
        return distance_total 

    #fitness function 1/distance
    def fitnessFun(self):
        return lambda life: 1.0 / self.distance(life.gene)


    def GA_run(self, n = 0):
        global task_allocation_record,  distance_total , task_allocation, best_chromosome
        while n > 0:
            self.ga.nextGeneration()
            distance = self.distance(self.ga.best.gene)
            print (("%d : %f") % (self.ga.generation, distance))
            print 'Chromosome task sorting:', self.ga.best.gene
            distance_total = distance
            best_chromosome = self.ga.best.gene 
            n -= 1
        
        print "Generation times %d,the best distance:%f"%(self.ga.generation, distance)
        task_allocation = {0:self.ga.best.gene[0:3],
                           1:self.ga.best.gene[3:6],
                           2:self.ga.best.gene[6:9],
                           3:self.ga.best.gene[9:12],
                           4:self.ga.best.gene[12:15],
                           5:self.ga.best.gene[15:18],
                           6:self.ga.best.gene[18:21],
                           7:self.ga.best.gene[21:]}
        print "Task Allocation:",task_allocation
        task_allocation_record =  copy.deepcopy(task_allocation) 
        
        
    def eachAgentTask(self):
        global task_allocation
        for i in self.agents:
            i.shelf_num = task_allocation[i.agent_id][0]
            task_allocation[i.agent_id].pop(0)
            
            

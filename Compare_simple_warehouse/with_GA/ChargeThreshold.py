import Strategy


class AgentCharge():

    def __init__(self, agents, graph, goods, graph_nodes, threshold_energy, consuming_rate, charging_rate):
        self.agents = agents
        self.graph = graph
        self.goods = goods
        self.graph_nodes = graph_nodes
        self.threshold_energy = threshold_energy
        self.consuming_rate = consuming_rate
        self.charging_rate = charging_rate

    def eleconsume(self, agent_id):
        if self.agents[agent_id].consume_mark == 1:
            self.agents[agent_id].step_times += 1
            self.agents[agent_id].consume_energy = (self.consuming_rate * 
                self.agents[agent_id].step_times)
            self.agents[agent_id].current_energy = self.agents[
                agent_id].full_energy - self.agents[agent_id].consume_energy
    #         print '!!!', r.agent_id, '???', r.current_energy
    
            if self.agents[agent_id].current_energy <= self.threshold_energy:
                #                 print r.agent_id
                if self.agents[agent_id].current_energy <= 0:
                    pass
#                     print "agent_id", agent_id
#                     raw_input("error")
                elif (self.agents[agent_id].status != 0 and 
                      self.agents[agent_id].arrive_goods_position == 0 and 
                      self.agents[agent_id].goods_forward_letter== 0):
                    if self.agents[agent_id].back_to_charge == 0:
                        if self.agents[agent_id].first_time_mark == 0:
                            self.agents[agent_id].first_time_mark = 1
                            # record status takeoff good or go back to charge
                            self.agents[agent_id].current_status = self.agents[
                                agent_id].status
                            self.agents[agent_id].need_charge_mark = 1
                            #blink red and orange
                        if self.agents[agent_id].current_status == 2:
                            if self.agents[agent_id].step_times % 20 == 0:
                                self.agents[agent_id].color = 2
                            elif self.agents[agent_id].step_times % 10 == 0:
                                self.agents[agent_id].color = 4
                    else: #blink blue and orange
                        if self.agents[agent_id].step_times % 20 == 0:
                            self.agents[agent_id].color = 1
                        elif self.agents[agent_id].step_times % 10 == 0:
                            self.agents[agent_id].color = 4

    def charging(self, agent_id):
        if self.agents[agent_id].full_energy_mark != 1:

            self.agents[agent_id].charge_times += 1
            self.agents[agent_id].charg_energy = self.charging_rate * 1
            self.agents[
                agent_id].current_energy += self.agents[agent_id].charg_energy
            if self.agents[agent_id].current_energy >= self.agents[agent_id].full_energy:
                self.agents[agent_id].full_energy_mark = 1
            # blink green and orange
            else:
                if self.agents[agent_id].charge_times % 20 == 0:
                    self.agents[agent_id].color = 0
                elif self.agents[agent_id].charge_times % 10 == 0:
                    self.agents[agent_id].color = 4

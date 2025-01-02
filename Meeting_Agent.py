from MGM import MGM


class Meeting(MGM):
    def __init__(self, id_, time_slot, dcop_id, meeting_individual_costs_dict, meeting_total_costs_dict):
        MGM.__init__(self,id_,time_slot, dcop_id)
        self.individual_costs = meeting_individual_costs_dict
        self.unary_constraint = meeting_total_costs_dict

    def compute(self):
        """Calculates the maximum local reduction by exploring all possible assignments and
         determines the best assignment that minimizes local cost."""
        self.lr = 0
        current_local_cost = self.calc_local_cost()
        min_possible_local_cost = current_local_cost
        best_local_assignment = self.variable

        for optional_asgmt in self.domain:
            current_costs = self.unary_constraint[optional_asgmt]
            for neighbor_id, neighbor_asgmt in self.neighbors_assignments.items():
                constraint = self.constraints[neighbor_id]
                if self.id_ < neighbor_id:
                    cost = constraint[(("A_"+str(self.id_), optional_asgmt), ("A_"+str(neighbor_id), neighbor_asgmt))]
                else:
                    cost = constraint[(("A_"+str(neighbor_id), neighbor_asgmt), ("A_"+str(self.id_), optional_asgmt))]
                current_costs += cost

            if current_costs < min_possible_local_cost:
                min_possible_local_cost = current_costs
                best_local_assignment = optional_asgmt

        # If a lower local cost is found with a different assignment, calculate the local reduction
        if min_possible_local_cost < current_local_cost:
            self.lr = current_local_cost - min_possible_local_cost
            self.lr_potential_asgmt = best_local_assignment

    def calc_local_cost(self):
        """Calculates the local cost based on the current variable assignment and neighbors' assignments context."""
        local_cost = self.unary_constraint[self.variable]
        for neighbor_id, neighbor_variable in self.neighbors_assignments.items():
            constraint = self.constraints[neighbor_id]
            if self.id_ < neighbor_id:
                cost = constraint[(("A_"+str(self.id_), self.variable), ("A_"+str(neighbor_id), neighbor_variable))]
            else:
                cost = constraint[(("A_"+str(neighbor_id), neighbor_variable), ("A_"+str(self.id_), self.variable))]
            local_cost += cost
        return local_cost



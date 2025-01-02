from Explanation import Explanation, calc_global_cost
from MGM import MGM_Status


class MGM_Explanation(Explanation):

    def __init__(self, dcop, category_1_agents, category_2_agents, category_3_agents, category_4_agents):
        """
        Initializes the MGM_Explanation instance, validating the agent categories.

        Args:
            dcop: A solved DCOP instance (i.e., given context).
            category_1_agents: List of agent IDs in Category 1 (constrained to context assignment).
            category_2_agents: List of agent IDs in Category 2 (free to select any value except the context assignment).
            category_3_agents: Dict of agent IDs in Category 3 (constrained to specific non-context assignment).
            category_4_agents: List of agent IDs in Category 4 (completely free to select any value).
        """
        Explanation.__init__(self, dcop, category_1_agents, category_2_agents, category_3_agents, category_4_agents)
        self.validate_k_limit_on_categories(k=1)

    def update_agents_before_generate_no_good(self):
        """Resets relevant fields for each agent before generating a no-good clause."""
        self.update_agent_domains()
        for agent in self.dcop.agents:
            # Reset local reduction variables and status for each agent
            agent.lr = None
            agent.lr_potential_asgmt = agent.variable
            agent.local_clock = 0
            agent.status = MGM_Status.wait_for_neighbors_assignments

    def generate_no_good(self):
        """Executes the DCOP and captures the no-good clause and its global cost."""
        self.dcop.execute()
        self.no_good = {agent.id_: agent.variable for agent in self.dcop.agents}
        self.no_good_global_cost = calc_global_cost(self.dcop)

    def explain(self):
        """Prints a detailed explanation of the context assignments, 
          no-good clause, global costs, and differences in global costs and in implicit constraints 
          between the context and the no-good clause.
          """
        print("Context assignments:")
        for agent, variable in self.context.items():
            print(f'    MGM_Agent_{agent} - {variable}')
        print("")
        print(f"Context global cost is: {self.context_global_cost}")
        print("")
        for agent, variable in self.no_good.items():
            print(f'    MGM_Agent_{agent} - {variable}')
        print("")
        print(f"No-Good global cost is: {self.no_good_global_cost}")
        print("")
        print(f"Therefore the exceed cost comparing to the context the query base on is:"
              f" {self.no_good_global_cost-self.context_global_cost}")
        print("")
        print("Implicit constraints differences:")
        print("")

        # Iterate over agents and their neighbors to compare the implicit constraints of the context and the no-good
        for agent in self.dcop.agents:
            agent_former_assignment = self.context[agent.id_]
            agent_assignment = self.no_good[agent.id_]
            for neighbor in agent.neighbors_agents_id:
                neighbor_former_assignment = self.context[neighbor]
                neighbor_assignment = self.no_good[neighbor]
                if not (neighbor_former_assignment == neighbor_assignment and
                        agent_former_assignment == agent_assignment):
                    constraint = agent.constraints[neighbor]
                    if agent.id_ < neighbor:
                        # Fetch former and current implicit constraints for comparison
                        former_implicit_constraint = constraint[(("A_" + str(agent.id_), self.context[agent.id_]),
                                                                 ("A_" + str(neighbor), self.context[neighbor]))]
                        current_implicit_constraint = constraint[(("A_" + str(agent.id_), self.no_good[agent.id_]),
                                                                  ("A_" + str(neighbor), self.no_good[neighbor]))]
                        print(f"    Constraint of A_{agent.id_} and  A_{neighbor} :")
                        print(f"        Former implicit constraint {former_implicit_constraint}")
                        print(f"        Current implicit constraint {current_implicit_constraint}")
                        print("")


class Meeting_Scheduling_Explanation(MGM_Explanation):
    def __init__(self, dcop, category_1_agents, category_2_agents, category_3_agents, category_4_agents):
        """
        Initializes the Meeting_Scheduling_Explanation instance, validating the agent categories.

        Args:
            dcop: A solved DCOP instance (i.e., given context).
            category_1_agents: List of Meetings IDs in Category 1 (constrained to context assignment).
            category_2_agents: List of Meetings IDs in Category 2 (free to select any value except the context assignment).
            category_3_agents: Dict of Meetings IDs in Category 3 (constrained to specific non-context assignment).
            category_4_agents: List of Meetings IDs in Category 4 (completely free to select any value).
        """
        MGM_Explanation.__init__(self, dcop, category_1_agents, category_2_agents, category_3_agents, category_4_agents)

    def explain(self, informative=False):
        """
        Explains the scenario in two modes:
        - As a story (informative=True) for a narrative explanation.
        - Not as a story (informative=False) for a straightforward technical explanation.
        """
        if informative:
            self.explain_as_story()
        else:
            self.explain_not_as_story()

    def explain_not_as_story(self):
        """
        Provides a detailed technical explanation of:
        - Context assignments
        - alternative assignments
        - Global costs and the cost difference
        - Implicit constraints that exist in either the context or the no-good clause but not in both (symmetric difference).
        """
        print("Context assignments:")
        for meeting, variable in self.context.items():
            print(f'    Meeting_Agent_{meeting} - {variable}')
        print("")
        print(f"Context global cost is: {self.context_global_cost}")
        print("")
        for meeting, variable in self.no_good.items():
            print(f'    Meeting_Agent_{meeting} - {variable}')
        print("")
        print(f"Alternative global cost is: {self.no_good_global_cost}")
        print("")
        print(f"Therefore the exceed cost comparing to the context the query base on is:"
              f" {self.no_good_global_cost - self.context_global_cost}")
        print("")
        print("Implicit constraints differences:")
        print("")

        # Compare implicit constraints between the context and Alternative assignments
        for meeting in self.dcop.agents:
            meeting_former_assignment = self.context[meeting.id_]
            meeting_assignment = self.no_good[meeting.id_]
            for neighbor in meeting.neighbors_agents_id:
                neighbor_former_assignment = self.context[neighbor]
                neighbor_assignment = self.no_good[neighbor]
                # Show implicit constraints only when there is a difference in assignments
                # between the context and the alternative clause for either the meeting or its neighbor.
                if not (neighbor_former_assignment == neighbor_assignment and
                        meeting_former_assignment == meeting_assignment):
                    constraint = meeting.constraints[neighbor]
                    if meeting.id_ < neighbor:  # To avoid duplicate comparisons
                        # Fetch and compare implicit constraints
                        former_implicit_constraint = constraint[(("A_" + str(meeting.id_), meeting_former_assignment),
                                                                 ("A_" + str(neighbor), neighbor_former_assignment))]
                        current_implicit_constraint = constraint[(("A_" + str(meeting.id_), meeting_assignment),
                                                                  ("A_" + str(neighbor), neighbor_assignment))]
                        print(f"    Constraint of Meeting_{meeting.id_} and  Meeting_{neighbor} :")
                        print(f"        Former implicit constraint {former_implicit_constraint}")
                        print(f"        Current implicit constraint {current_implicit_constraint}")
                        print("")

            # Compare unary constraints only when there is a difference in assignments
            # between the context and the alternative
            if meeting_former_assignment != meeting_assignment:
                print(f"    Unary Constraint of Meeting_{meeting.id_} :")
                print(f"        Former Unary constraint {meeting.unary_constraint[meeting_former_assignment]}")
                print(f"        Current Unary constraint {meeting.unary_constraint[meeting_assignment]}")

    def explain_as_story(self):
        """
        Provides a narrative explanation of:
        - Context and Alternative assignments
        - Global costs and cost differences
        - Implicit constraint differences and their impact
        - How participant satisfaction changes.
        """
        print("Context assignments:")
        for meeting, variable in self.context.items():
            print(f'    Meeting_Agent_{meeting} - {variable}')
        print("")
        print(f"Context global cost is: {self.context_global_cost}")
        print("")
        print("Alternative assignments:")
        for meeting, variable in self.no_good.items():
            print(f'    Meeting_Agent_{meeting} - {variable}')
        print("")
        print(f"Alternative global cost is: {self.no_good_global_cost}")
        print("")
        print(f"Therefore, the exceed cost compared to the context is: {self.no_good_global_cost - self.context_global_cost}")
        print("")
        print("Implicit constraints differences:")
        print("")

        # Compare implicit constraints and narrate the impact on relationships
        for meeting in self.dcop.agents:
            meeting_former_assignment = self.context[meeting.id_]
            meeting_assignment = self.no_good[meeting.id_]
            for neighbor in meeting.neighbors_agents_id:
                neighbor_former_assignment = self.context[neighbor]
                neighbor_assignment = self.no_good[neighbor]
                # Show implicit constraints only when there is a difference in assignments
                # between the context and the alternative clause for either the meeting or its neighbor.
                if not (neighbor_former_assignment == neighbor_assignment and
                        meeting_former_assignment == meeting_assignment):
                    constraint = meeting.constraints[neighbor]
                    if meeting.id_ < neighbor:  # Avoid duplicate comparisons
                        # Determine if meetings overlapped before or after the change
                        overlap_before = meeting_former_assignment == neighbor_former_assignment
                        overlap_after = meeting_assignment == neighbor_assignment

                        # Identify shared participants between the meetings
                        shared_agents = set(meeting.individual_costs.keys()).intersection(
                            self.dcop.agents[neighbor - 1].individual_costs.keys())
                        shared_agents_list = ", ".join(f"Agent {agent_id}" for agent_id in shared_agents)

                        # Narrate the relationship changes due to overlap
                        if not overlap_after:
                            if overlap_before:
                                story = (
                                    f"Meetings overlapped before the change, but after the time slot change, they no longer overlap. "
                                    f"Mutual participants ({shared_agents_list}) can now participate in both meetings."
                                )
                            else:
                                story = (
                                    f"Meetings did not overlap before or after the change. "
                                    f"Mutual participants ({shared_agents_list}) could already participate in both meetings."
                                )
                        else:
                            if overlap_before:
                                story = (
                                    f"Meetings overlapped before the change, and they still overlap after the time slot change. "
                                    f"Mutual participants ({shared_agents_list}) cannot participate in both meetings simultaneously."
                                )
                            else:
                                story = (
                                    f"Meetings did not overlap before the change, but after the time slot change, they now overlap. "
                                    f"Mutual participants ({shared_agents_list}) can no longer participate in both meetings."
                                )

                        print(
                            f"    Influence of the time slot change on the relationship between Meeting_{meeting.id_} and Meeting_{neighbor}:")
                        print(f"        {story}")
                        print("")

            # Compare and narrate changes in participant satisfaction
            if meeting_former_assignment != meeting_assignment:
                print(
                    f"    Influence of the time slot change on the satisfaction of participants in Meeting_{meeting.id_}:")
                # Fetch total costs from the unary_constraint field
                total_cost_before = meeting.unary_constraint[meeting_former_assignment]
                total_cost_after = meeting.unary_constraint[meeting_assignment]

                # Determine the trend in total satisfaction
                if total_cost_after < total_cost_before:
                    total_satisfaction_trend = "increased"
                elif total_cost_after > total_cost_before:
                    total_satisfaction_trend = "reduced"
                else:
                    total_satisfaction_trend = "remained the same"

                for agent_id, time_slot_costs in meeting.individual_costs.items():
                    former_cost = time_slot_costs[meeting_former_assignment]
                    current_cost = time_slot_costs[meeting_assignment]

                    # Determine the impact
                    if current_cost < former_cost:
                        impact = f"reduced from {former_cost} to {current_cost}"
                    elif current_cost > former_cost:
                        impact = f"increased from {former_cost} to {current_cost}"
                    else:
                        impact = f"remained the same at {former_cost}"

                    # Explain the impact for each participant
                    print(f"        Agent {agent_id}: Cost {impact}")

                # Summarize total satisfaction changes
                if total_cost_before == total_cost_after:
                    print(
                        f"        Total satisfaction of participants in Meeting_{meeting.id_} remained the same at {total_cost_before}.")
                else:
                    print(
                        f"        Total satisfaction of participants in Meeting_{meeting.id_} changed from {total_cost_before} to {total_cost_after} (lower is better).")
                print(f"        The overall satisfaction trend for Meeting_{meeting.id_} is: {total_satisfaction_trend}.")

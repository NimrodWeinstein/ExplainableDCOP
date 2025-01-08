import copy

from Meeting_Agent import Meeting
from problems import *


class DCOP_MeetingScheduling(DCOP):
    def __init__(self, id_, A, D, dcop_name, algorithm, min_meeting_participant=2):
        DCOP.__init__(self, id_, A, D, dcop_name, algorithm)
        self.M = meetings
        self.meetings_per_agent = meetings_per_agent
        self.min_meeting_participant = min_meeting_participant

        if A * meetings_per_agent < meetings * min_meeting_participant:
            raise ValueError("Not enough agents to fulfill minimum meeting participants.")
        if meetings_per_agent > meetings:
            raise ValueError("meetings_per_agent cannot exceed the total number of meetings.")

        self.rnd_meetings_assignments = random.Random((id_+6)*17)


        # Generate agent assignments to meetings
        self.agent_meetings = {agent_id: set() for agent_id in range(1, self.A + 1)}
        self.meeting_participants = {meeting_id: set() for meeting_id in range(1, self.M + 1)}

        # Assign minimum participants to each meeting
        self.assign_minimum_participants_to_meetings()

        # Assign each agent to the required number of meetings
        self.assign_agents_to_meetings()

        # Create unary costs for each agent
        self.create_unary_costs_for_agents()

        # Meeting costs for individual agents
        self.meeting_individual_costs = self.create_meeting_agent_costs()

        # Aggregate meeting costs
        self.meeting_total_costs = self.aggregate_meeting_costs()

        # Find pairs of meetings with mutual participants
        self.meeting_neighbors = self.find_meeting_with_mutual_participants()

        self.original_agents = copy.deepcopy(self.agents)
        self.agents = [] # meeting agents
        self.create_meetings()
        self.neighbors = []
        self.create_meetings_neighbors()
        self.connect_agents_to_neighbors()
        self.mailer = Mailer(self.agents)
        self.global_clock = 0
        self.inform_root()
        self.records_dcop = {}

    def assign_minimum_participants_to_meetings(self):
        """
        Ensures each meeting has at least the minimum number of participants.
        """
        meeting_id=1 # Start with the first meeting
        while meeting_id<=self.M:
            while len(self.meeting_participants[meeting_id]) < self.min_meeting_participant:
                # Find agents eligible to join the current meeting
                available_agents = [
                    agent_id for agent_id in range(1, self.A + 1)
                    if len(self.agent_meetings[agent_id]) < self.meetings_per_agent and
                         agent_id not in self.meeting_participants[meeting_id]]
                # If no eligible agents are found, handle the issue
                if not available_agents:
                    # Check if the overall parameters can theoretically allow for a valid assignment
                    if self.meetings_per_agent*self.A >= self.M*self.min_meeting_participant:
                        self.agent_meetings = {agent_id: set() for agent_id in range(1, self.A + 1)}
                        self.meeting_participants = {meeting_id: set() for meeting_id in range(1, self.M + 1)}
                        meeting_id = 0
                        break  # Exit the current loop to restart the assignment process
                    else:
                        # If parameters are inherently invalid, raise an error
                        raise ValueError("Not enough agents available to meet constraints.")
                # Randomly select an eligible agent to participate in the current meeting
                candidate_agent = self.rnd_meetings_assignments.choice(available_agents)
                self.meeting_participants[meeting_id].add(candidate_agent)
                self.agent_meetings[candidate_agent].add(meeting_id)

            # Move to the next meeting after successfully assigning participants
            meeting_id += 1

    def assign_agents_to_meetings(self):
        """
        Ensures each agent is assigned to the required number of meetings.
        """
        for agent_id in range(1, self.A + 1):
            while len(self.agent_meetings[agent_id]) < self.meetings_per_agent:
                # Select meetings that do not already include the agent and do not include more agents than possible
                available_meetings = [
                    meeting_id for meeting_id in range(1, self.M + 1)
                    if
                    len(self.meeting_participants[meeting_id]) < self.A and agent_id not in self.meeting_participants[meeting_id]
                ]
                if not available_meetings:
                    raise ValueError("Not enough meetings available to meet constraints.")
                candidate_meeting = self.rnd_meetings_assignments.choice(available_meetings)
                self.meeting_participants[candidate_meeting].add(agent_id)
                self.agent_meetings[agent_id].add(candidate_meeting)

    def create_unary_costs_for_agents(self):
        """
        Calls the `create_unary_costs` method for each agent in the DCOP_MeetingScheduling instance.
        This initializes the unary costs for all agents.
        """
        for agent in self.agents:
            agent.create_unary_costs(self.dcop_id)

    def create_meeting_agent_costs(self):
        """
        Creates a dictionary mapping each meeting ID to a dictionary of agent IDs and their time slot costs.
        Returns:
            dict: A dictionary where keys are meeting IDs, and values are dictionaries of agent IDs mapping to their time slot costs.
        """
        meeting_agent_costs = {}

        # Iterate through each meeting
        for meeting_id in self.meeting_participants.keys():
            agent_costs = {}

            # Get the agents participating in this meeting
            participants = self.meeting_participants[meeting_id]

            for agent_id in participants:
                agent = self.agents[agent_id - 1]
                agent_costs[agent_id] = agent.unary_constraint  # Assign the agent's time slot costs

            meeting_agent_costs[meeting_id] = agent_costs

        return meeting_agent_costs

    def aggregate_meeting_costs(self):
        """
        Aggregates the sum of unary costs for all agents for each meeting at every time slot.
        Utilizes the `create_meeting_agent_costs` method to get agent costs for meetings.
        Returns:
            dict: A dictionary where keys are meeting IDs and values are dictionaries of time slots and their aggregated costs.
        """
        # Initialize a dictionary for each meeting with time slot costs starting from 0
        meeting_costs = {meeting_id: {time_slot: 0 for time_slot in range(self.D)}
                         for meeting_id in range(1, self.M + 1)}

        # Get the agent costs for each meeting
        meeting_agent_costs = self.meeting_individual_costs

        # Aggregate costs for each time slot in each meeting
        for meeting_id, agent_costs in meeting_agent_costs.items():
            for agent_id, time_slot_costs in agent_costs.items():
                for time_slot, cost in time_slot_costs.items():
                    meeting_costs[meeting_id][time_slot] += cost

        return meeting_costs

    def find_meeting_with_mutual_participants(self):
        """
        Finds pairs of meetings that share at least one mutual participant.
        Returns:
            list: A sorted list of unique pairs of meeting IDs that share mutual participants.
        """
        meeting_pairs = set()  # Use a set to avoid duplicate pairs

        # Iterate through all pairs of meetings
        for meeting1, participants1 in self.meeting_participants.items():
            for meeting2, participants2 in self.meeting_participants.items():
                if meeting1 < meeting2:  # Avoid duplicate and self-comparison
                    # Check if the two meetings share at least one participant
                    if participants1 & participants2:  # Set intersection to find mutual participants
                        meeting_pairs.add((meeting1, meeting2))  # Add the pair as a neighbor

        # Convert to a sorted list if needed for consistent order
        meeting_pairs = sorted(meeting_pairs)

        return meeting_pairs

    def create_meetings(self):
        for i in range(self.M):
            if self.algorithm == Algorithm.branch_and_bound:
                self.agents.append(BranchAndBound(i + 1, self.D))
            if self.algorithm == Algorithm.MGM:
                self.agents.append(Meeting(i + 1, self.D, self.dcop_id, self.meeting_individual_costs[i + 1],
                                           self.meeting_total_costs[i + 1]))

    def create_meetings_neighbors(self):
        """
        Creates neighbors between meetings based on mutual participants.
        Adds a Neighbors object for each pair of meetings with a non-equal cost function.
        """
        for meeting_neighbor in self.meeting_neighbors:
            self.neighbors.append(
                Neighbors(
                    self.agents[meeting_neighbor[0]-1],  # Meeting 1
                    self.agents[meeting_neighbor[1]-1],  # Meeting 2
                    meeting_scheduling_must_be_non_equal_cost_function,  # Cost function
                    self.dcop_id  # DCOP ID
                )
            )

    def create_neighbors(self):
        pass

    def __str__(self):
        """
        Returns a detailed and clean description of the scenario in a story-like format.
        """
        story = [
            f"Scenario Details:",
            f"------------------",
            f"There are {self.M} meetings to be scheduled, with a total of {self.A} agents involved.",
            f"Each agent is assigned to participate in {self.meetings_per_agent} meetings.",
            f"Each meeting must have at least {self.min_meeting_participant} participants.",
            f"The problem includes {self.D} available time slots for scheduling.",
            "",
            f"Meeting Participants:",
        ]
        # Add details of participants for each meeting
        for meeting_id, participants in self.meeting_participants.items():
            participant_list = ", ".join(f"Agent {agent_id}" for agent_id in sorted(participants))
            story.append(
                f"  - Meeting {meeting_id}: {participant_list if participant_list else 'No participants assigned'}")

        story.append("")
        story.append("Satisfaction for each participant is determined by their preferences: lower costs indicate higher satisfaction.")
        story.append("")
        story.append("Participants Satisfaction Constraints:")
        story.append("-------------------------")

        # Add unary constraints for each agent
        for agent in self.original_agents:
            constraints = ", ".join(f"Slot {slot}: {cost}" for slot, cost in agent.unary_constraint.items())
            story.append(f"  - Agent {agent.id_}: {constraints if constraints else 'No constraints defined'}")

        story.append("\n-------------------------------------------------------------------------"
                     "------------------------------------------")

        return "\n".join(story)

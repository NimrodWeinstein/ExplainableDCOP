from Globals_ import *
from MGM_Explanation import Meeting_Scheduling_Explanation
from problems import *
from Explanation import calc_global_cost
from MeetingScheduling import DCOP_MeetingScheduling


def create_selected_dcop(i,dcop_type,algorithm):
    if dcop_type == DcopType.sparse_random_uniform:
        A = 5
        D = 10
        dcop_name = "Sparse Uniform"
        return DCOP_RandomUniform(i,A,D,dcop_name,algorithm)
    if dcop_type == DcopType.dense_random_uniform:
        A = 5
        D = 10
        dcop_name = "Dense Uniform"
        return DCOP_RandomUniform(i,A,D,dcop_name,algorithm)
    if dcop_type == DcopType.graph_coloring:
        A = 5
        D = 10
        dcop_name = "Graph Coloring"
        return DCOP_GraphColoring(i,A,D,dcop_name,algorithm)
    if dcop_type == DcopType.meeting_scheduling:
        A = 4
        dcop_name = "Meeting Scheduling"
        return DCOP_MeetingScheduling(i, A, time_slots_D, dcop_name, algorithm)


if __name__ == '__main__':
    dcop_type = DcopType.meeting_scheduling
    algorithm = Algorithm.MGM
    for i in range(repetitions):
        dcop = create_selected_dcop(i,dcop_type,algorithm)
        #print(f"Initially global cost is: {calc_global_cost(dcop)}")
        dcop.execute()
        print()
        print(dcop)
        print()
        First_Explanation= Meeting_Scheduling_Explanation(dcop, [1,2,3], [4], {}, [])
        First_Explanation.update_agents_before_generate_no_good()
        First_Explanation.generate_no_good()
        First_Explanation.explain(informative=True)


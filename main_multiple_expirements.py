import matplotlib.pyplot as plt

from Globals_ import *
from problems import *




def create_selected_dcop(i,A,D,dcop_name):
    if dcop_type == DcopType.sparse_random_uniform:
        return DCOP_RandomUniform(i,A,D,dcop_name)
    if dcop_type == DcopType.graph_coloring:
        return DCOP_GraphColoring(i,A,D,dcop_name)



def solve_dcops(dcops):
    for dcop in dcops:
        draw_dcop(dcop)
        dcop.execute()
        draw_result(dcop)






if __name__ == '__main__':
    A,D,dcop_name = given_dcop_create_input()
    dcops = []
    for i in range(repetitions):
        dcops.append(create_selected_dcop(i,A,D,dcop_name))
    solve_dcops(dcops)
    #create_data(dcops)

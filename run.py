import copy
import imp

from kuromasu import Kuromasu


filename = 'in.txt'

def get_data_from_file(filename):
    with open(filename) as f:
        global data
        data = imp.load_source('data', '', f)

get_data_from_file(filename)
for i, board in enumerate(data.BOARDS):
    print("BOARD #{}:".format(i))
    print("=" * 50)

    print("DFS:")
    result, steps, instances = Kuromasu.solve_dfs(copy.deepcopy(board))
    print(result)
    print("step count: ", steps)
    print("instances created: ", instances)
    print()

    Kuromasu.reset()
    print("A*:")
    result, steps, instances = Kuromasu.solve_a_star(copy.deepcopy(board))
    print(result)
    print("step count: ", steps)
    print("instances created: ", instances)
    print() 

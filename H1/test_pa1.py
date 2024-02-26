from problem import *
from search_algorithms import *
from collections import Counter

"""
    We will use cProfile to get some function call stats. 
    Particularly, we want to count the number of times a node is popped from frontier and is generated. 
    To count the number of times a node is popped, we just need to count number of times pop() is called.
    To count number of times a node is generated, notice that we call p.result.
    So, we just need to count number of times result is called for a Problem object.
"""
import cProfile, pstats, io
from pstats import SortKey   
def run_profiler_searches(problem, searchers_list, searcher_names_list):
    problem_name = str(problem)[:28]
    total_gen_node, total_pop_node = 0, 0
    print('\nProfiler for problem: {}\n'.format(problem_name))
    for search_algo, search_algo_name in zip(searchers_list, searcher_names_list):
        pr = cProfile.Profile()
        pr.enable()
        goal_node = search_algo(problem)
        pr.disable()
        
        io_stream = io.StringIO()
        ps = pstats.Stats(pr, stream=io_stream).sort_stats(SortKey.CALLS).strip_dirs()
        ps.print_stats("pop*|result*")
        profiler_string = io_stream.getvalue()
        
        gen_node_count, pop_node_count = profiler_splitter(profiler_string)
        total_gen_node += gen_node_count
        total_pop_node += pop_node_count
        
    
        print('{:15s} {:9,d} generated nodes |{:9,d} popped |{:5.0f} solution cost |{:8,d} solution depth|'.format(
              search_algo_name, gen_node_count, pop_node_count, goal_node.path_cost, goal_node.depth))
    
    
    print('{:15s} {:9,d} generated nodes |{:9,d} popped'.format('TOTAL', total_gen_node, total_pop_node))
    print('________________________________________________________________________')

def profiler_splitter(profiler_data):
    profiler_data = profiler_data.split("\n")
    result_line = [l for l in profiler_data if 'result' in l][1]
    pop_line = [l for l in profiler_data if 'pop' in l][1]
    
    splitter = (lambda s: int(s.split()[0].split("/")[0]) )
    result_calls = splitter(result_line)
    pop_calls = splitter(pop_line)
    
    return result_calls, pop_calls 
    
if __name__ == "__main__":
    # route problem example
    example_map_edges = { ('R', 'D'): 410,
                        ('R', 'H'): 620,
                        ('R', 'J'): 950,
                        ('R', 'A'): 950,
                        ('D', 'B'): 110,
                        ('H', 'B'): 940,
                        ('H', 'T'): 680,
                        ('B', 'T'): 1600,
                        ('J', 'A'): 680,
                        ('J', 'Y'): 330,
                        ('Y', 'T'): 680
                        }

    example_coords = {'A': (0,200),
                      'B': (1250,600), 
                      'D': (1300,550),
                      'H': (500,850),
                      'J': (100,450),
                      'T': (0,1300),
                      'R': (950,500),
                      'Y': (50,750)
                      }

    example_must_visit = ['R', 'H', 'T', 'Y']


    example_route_problem = VariantRouteProblem(initial_agent_loc='D', goal_loc='J', 
                                                 map_edges=example_map_edges, 
                                                 map_coords=example_coords, 
                                                 must_visit =example_must_visit,
                                                 K=5)

    example_state = ('R', False, False, 1, True, False, False, False)
    print('For VariantRouteProblem. From state: {}. we have the following actions available:'.format(example_state))
    actions_available = example_route_problem.actions(state=example_state)
    print(actions_available)
    print('For VariantRouteProblem. From state: {}. Taking action: {}'.format(example_state, 'H'))
    next_state = example_route_problem.result(state=example_state, action='H')
    print(next_state)
    print('________________________________________________________________________')
    
    # grid problem example
    example_monster_coords = [(5,2), (3,3), (1,2)] 

    example_grid_problem = GridHunterProblem(initial_agent=(4,5, 'north'), 
                                             N=5, 
                                             monster_coords=example_monster_coords)
    
    example_state = (5, 5, 'north', True, 0, True, True, False)
    print('For GridHunterProblem. From state: {}. we have the following actions available:'.format(example_state))
    actions_available = example_grid_problem.actions(state=example_state)
    print(actions_available)
    print('For GridHunterProblem. From state: {}. Taking action: {}'.format(example_state, 'move-forward'))
    next_state = example_grid_problem.result(state=example_state, action='move-forward')
    print(next_state)
    
    example_state = (5, 5, 'west', True, 3, False, False, False)
    print('For GridHunterProblem. From state: {}. Taking action: {}'.format(example_state, 'shoot-arrow'))
    next_state = example_grid_problem.result(state=example_state, action='shoot-arrow')
    print(next_state)
    
    example_state = (5, 1, 'north', True, 0, False, False, False)
    print('For GridHunterProblem. From state: {}. Taking action: {}'.format(example_state, 'shoot-arrow'))
    next_state = example_grid_problem.result(state=example_state, action='turn-left')
    print(next_state)
    print('________________________________________________________________________')
    
    # add your own problems and try printing report. 
    goal_node = uniform_cost_search(example_route_problem)
    print('printing solution path for route problem')
    print(get_path_states(goal_node))
    print('printing solution-actions-path')
    print(get_path_actions(goal_node))
    print('________________________________________________________________________')
    print('________________________________________________________________________')
    
    ######## #######
    
    # get some statistics on generated nodes, popped nodes, solution
    
    searchers = [(lambda p: breadth_first_search(p, treelike=False)), 
                 (lambda p: breadth_first_search(p, treelike=True)), 
                 (lambda p: uniform_cost_search(p, treelike=False)), 
                 (lambda p: uniform_cost_search(p, treelike=True)),  
                 (lambda p: astar_search(p, h=p.h, treelike=False)), 
                 (lambda p: astar_search(p, h=p.h, treelike=True))]
    searcher_names= ['Graph-like BFS', 'Tree-like BFS', 
                     'Graph-like UCS', 'Tree-like UCS', 
                     'Graph-like A*', 'Tree-like A*']
    
    run_profiler_searches(example_route_problem, searchers, searcher_names)
    run_profiler_searches(example_grid_problem, searchers, searcher_names)

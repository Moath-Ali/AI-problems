import heapq
from problem import *

class Node:
    def __init__(self,state, parent_node=None,action_from_parent=None, path_cost=0):
        self.state = state
        self.parent_node = parent_node
        self.action_from_parent = action_from_parent
        self.path_cost = path_cost
        if parent_node==None:
            self.depth = 0
        else:
            self.depth = parent_node.depth + +1
    
    def __lt__(self, other):
        return self.state < other.state
    

class PriorityQueue:
 def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
        # add the items to the PQ
        for item in items:
            self.add(item)

 """
 Add item to PQ with priority-value given by call to priority_function
 """
 def add(self, item):
    pair = (self.priority_function(item), item)
    heapq.heappush(self.pqueue, pair)
    """
    pop and return item from PQ with min priority-value
    """
 def pop(self):
     return heapq.heappop(self.pqueue)[1]
 """
 gets number of items in PQ
 """
 def __len__(self):
    return len(self.pqueue)
 



def expand(problem,node):
    s0 = node.state
    l = []
    for action in problem.actions(s0):
        s1 = problem.result(s0,action)
        cost = node.path_cost + problem.action_cost(s0,action,s1)
        l.append(Node(state=s1,parent_node=node,action_from_parent=action,path_cost=cost))

    return l

def get_path_actions(node):
    l = []
    
    tNode = node
    if(tNode == None):
        return []
    else:
        while tNode.parent_node != None:
            l.append(tNode.parent_node.state[0])
            tNode = tNode.parent_node
            if tNode == None:
                l.append(tNode.state[0])

        
        l.reverse()
        l.insert(len(l),node.state[0])
        return l[1:]
    
def get_path_states(node):
    l = []
    
    tNode = node
    if(tNode == None):
        return []
    else:
        while tNode.parent_node != None:
            l.append(tNode.parent_node.state)
            tNode = tNode.parent_node
            if tNode == None:
                l.append(tNode.state)

        
        l.reverse()
        l.insert(len(l),node.state)
        return l

def best_first_search(problem, f):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(items=(node,),priority_function=f)

    reached = {node.state:node}
    while len(frontier)>0:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node

        for child in expand(problem,node):
            s = child.state            
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return None

def best_first_search_treelike(problem,f):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue((),f)
    frontier.add(node)
    while len(frontier)>0:
        node = frontier.pop()

        if problem.is_goal(node.state):
            return node
        
        for child in expand(problem,node):

            s = child.state
            frontier.add(child)
    return None

def breadth_first_search(problem,treelike=False):
    if not treelike:
        return best_first_search(problem,lambda n: n.depth)
    else:
        return best_first_search_treelike(problem,lambda n: n.depth)

def depth_first_search(problem,treelike=False):
    if not treelike:
        return best_first_search(problem,lambda n:  0-n.depth)
    else:
        return best_first_search_treelike(problem,lambda n: 0-n.depth)

def uniform_cost_search(problem,treelike=False):
    if not treelike:
        return best_first_search(problem,lambda n: n.path_cost)
    else:
        return best_first_search_treelike(problem,lambda n: n.path_cost)

def greedy_search(problem, h, treelike=False):
    if not treelike:
        return best_first_search(problem,lambda n: h(n))
    else:
        return best_first_search_treelike(problem,lambda n: h(n))

def astar_search(problem, h, treelike=False):
    if not treelike:
        return best_first_search(problem,lambda n: n.path_cost + h(n))
    else:
        return best_first_search_treelike(problem,lambda n: n.path_cost + h(n))

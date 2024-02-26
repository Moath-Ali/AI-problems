example_map_edges = {
('R', 'D'): 410,
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

class VariantRouteProblem:
    def __init__(self,initial_agent_loc,goal_loc,map_edges,map_coords,must_visit,K):
        self.initial_agent_loc = initial_agent_loc
        self.map_edges = map_edges
        self.map_coords = map_coords
        self.must_visit = must_visit
        self.goal_loc = goal_loc
        self.K = K
        self.state = [initial_agent_loc,False,False,0]
        for i in must_visit:
            self.state.append(False)
        self.state = tuple(self.state)
        
        

    def actions(self,state):
        nList =[]
        for key in self.map_edges:
            if state[0] in key: #to get the loc
                nList.append(key) #this will return the neighbors
        
        return nList
    
    #𝑠𝑡𝑎𝑡𝑒 = (𝑙𝑜𝑐, 𝑔1, 𝑔2, 𝑘,𝑡1,𝑡2, … ,𝑡𝑀),
    #example_state = ('R', False, False, 1, True, False, False, False)
    #example_must_visit = ['R', 'H', 'T', 'Y']
    def result(self,state,action):
        found =False
        for i in self.actions(self.state):
            if action in i:
                found = True

        if action == self.state[0]:

            index = self.must_visit.index(action)
            temp = list(self.state)
            temp[3] += 1
            temp[index+4] = True #to change the must visit location status
            self.state = tuple(temp)
            return self.state

        elif found and action not in self.must_visit:
            #add +1 to k and change to new state
            temp = list(self.state)
            temp[0]=action
            temp[3] += 1
            self.state = tuple(temp)
            return self.state
            
        elif found and action in self.must_visit: #to check if the action in the must visit
            #change must visit

            index = self.must_visit.index(action)

            temp = list(self.state)
            temp[index+4] = True #to change the must visit location status
            temp[0] = action
            temp[3] += 1
            self.state = tuple(temp)
            return self.state
        
        return self.state
        
        #update the steps and the location

    
    def action_cost(self,state1,action,state2):

        temp0 = []
        temp0.append(state1[0])
        temp0.append(state2[0])
        temp0 = tuple(temp0)

        temp1=[]
        temp1.append(state2[0])
        temp1.append(state1[0])
        temp1 = tuple(temp1)


        if temp0 in self.map_edges:
            return self.map_edges[temp0]

        elif temp1 in self.map_edges:
           return self.map_edges[temp1]
        else:
            return "inf"


    def is_goal(self,state):
        s = self.state
        bol = True
        for i in range(self.state-4):
            if self.state[i+4] == False:
                bol = False

        if s[0]==self.goal_loc and bol and s[1] and not s[2] and s[3]<=self.K:
            return True
        else:
            return False
    def h(self,node):
        if(node.state[0]==node.goal_loc):
            return 0
        
        else:
            return (self.map_coords(node.state[0])[0]-self.map_coords(node.goal_loc)[0])**2 + (self.map_coords(node.state[0])[1]-self.map_coords(node.goal_loc)[1])**2






    

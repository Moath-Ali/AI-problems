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



class VariantRouteProblem:
    def __init__(self,initial_agent_loc,goal_loc,map_edges,map_coords,must_visit,K):
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
                nList.append(key[1]) #this will return the neighbors
        
        return nList
    
    #𝑠𝑡𝑎𝑡𝑒 = (𝑙𝑜𝑐, 𝑔1, 𝑔2, 𝑘,𝑡1,𝑡2, … ,𝑡𝑀),
    #example_state = ('R', False, False, 1, True, False, False, False)
    #example_must_visit = ['R', 'H', 'T', 'Y']
    def result(self,state,action):
        if action == state[0]:
            return
        elif action in self.must_visit: #to check if the action in the must visit
            index = self.must_visit.index(action)
            state[index+4] = True #to change the must visit location status
        
        #update the steps and the location
        self.state[0] = action
        self.state[3] += 1

    def s(self):
        return self.state



    
        
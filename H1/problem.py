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
                temp = list(key)
                if temp.index(state[0]) == 0:
                    nList.append(temp[1]) #this will return the neighbors
                else:
                    nList.append(temp[0])
                
        
        return nList
    
    #𝑠𝑡𝑎𝑡𝑒 = (𝑙𝑜𝑐, 𝑔1, 𝑔2, 𝑘,𝑡1,𝑡2, … ,𝑡𝑀),
    #example_state = ('R', False, False, 1, True, False, False, False)
    #example_must_visit = ['R', 'H', 'T', 'Y']
    def result(self,state,action):
        stateList = list(state)
        stateList[0] = action
        stateList[3] +=1
        
        if action in self.must_visit:
           stateList[self.must_visit.index(action)+4] = True
        
        if action == self.goal_loc and state[1] == True:
            stateList[2] = True
        if action == self.goal_loc:
            stateList[1] = True


        return tuple(stateList)


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
            return 0


    def is_goal(self,state):
        s = state
        bol = state[4:].count(True)>=(len(state)-4)/2

        if s[0]==self.goal_loc and bol and s[1] and not s[2] and s[3]<=self.K:
            return True
        else:
            return False
        

    def h(self,node):
        if(self.is_goal(node.state)):
            return 0
        
        else:
            return ((self.map_coords[(node.state)[0]][0] - self.map_coords[self.goal_loc][0])**2  + (self.map_coords[node.state[0]][1] - self.map_coords[self.goal_loc][1])**2)**0.5

class GridHunterProblem:

    def __init__(self, initial_agent, N, monster_coords):
        self.agentLocation = initial_agent
        self.N = N
        self.monsterCoords = monster_coords
        monStatus = []
        for i in range(1, len(monster_coords)+1):
            monStatus.append(False)
        agentList = list(initial_agent)
        stateList = agentList + [True, 0] + monStatus
        self.initial_state = tuple(stateList)
        self.state = self.initial_state
    
    def move_monsters(self, timestep):
        newmonsterCoords = self.monsterCoords
        monsterList = []
        for i in newmonsterCoords:
            monsterList.append(list(i))
        if timestep == 0:
            return newmonsterCoords
        elif timestep == 1:
            for i in monsterList:
                i[1] = i[1]-1
        elif timestep == 2:
            return newmonsterCoords
        elif timestep == 3:
            for i in monsterList:
                i[1] = i[1]+1
        newmonsterCoords = []
        for i in monsterList:
            newmonsterCoords.append(tuple(i))
        return newmonsterCoords

    def actions(self, state):
        if state[3] == False:
            return []

        if state[0] == self.N and state[2] == 'north':
            return ['turn-left', 'turn-right', 'shoot-arrow', 'stay']
        elif state[0] == 1 and state[2] == 'south':
            return ['turn-left', 'turn-right', 'shoot-arrow', 'stay']
        elif state[1] == 1 and state[2] == 'west':
            return ['turn-left', 'turn-right', 'shoot-arrow', 'stay']
        elif state[1] == self.N and state[2] == 'east':
            return ['turn-left', 'turn-right', 'shoot-arrow', 'stay']
        else:
            return ['move-forward', 'turn-left', 'turn-right', 'shoot-arrow', 'stay']
    
    def result(self, state, action):
        stateList = list(state)
        mstep = (state[4] + 1)%4
        newmonsterCoords = self.move_monsters(mstep)
        stateList[4] = mstep
        #self.state = tuple(stateList)
        if action == 'shoot-arrow':
            if stateList[2] == 'west':
                i = 0
                for monster in newmonsterCoords:
                    for arrow in range(stateList[1]-1,0,-1):
                        if monster[0] == stateList[0] and monster[1] == arrow:
                            stateList[i+5] = True
                    i += 1
            elif stateList[2] == 'east':
                i = 0
                for monster in newmonsterCoords:
                    for arrow in range(stateList[1]+1, self.N+1):
                        if monster[0] == stateList[0] and monster[1] == arrow:
                            stateList[i+5] = True
                    i += 1
            elif stateList[2] == 'north':
                i = 0
                for monster in newmonsterCoords:
                    for arrow in range(stateList[0]+1, self.N+1):
                        if monster[0] == arrow and monster[1] == stateList[1]:
                            stateList[i+5] = True
                    i += 1
            elif stateList[2] == 'south':
                i = 0
                for monster in newmonsterCoords:
                    for arrow in range(stateList[0]-1, 0, -1):
                        if monster[0] == arrow and monster[1] == stateList[1]:
                            stateList[i+5] = True
                    i += 1

        elif action == 'move-forward':
            if stateList[2] == 'north':
                stateList[0] = stateList[0] + 1
            elif stateList[2] == 'south':
                stateList[0] = stateList[0] - 1
            elif stateList[2] == 'east':
                stateList[1] = stateList[1] + 1
            elif stateList[2] == 'west':
                stateList[1] = stateList[1] - 1

        elif action == 'turn-right':
            if stateList[2] == 'north':
                stateList[2] = 'east'
            elif stateList[2] == 'east':
                stateList[2] = 'south'
            elif stateList[2] == 'south':
                stateList[2] = 'west'
            elif stateList[2] == 'west':
                stateList[2] = 'north'

        elif action == 'turn-left':
            if stateList[2] == 'north':
                stateList[2] = 'west'
            elif stateList[2] == 'west':
                stateList[2] = 'south'
            elif stateList[2] == 'south':
                stateList[2] = 'east'
            elif stateList[2] == 'east':
                stateList[2] = 'north'

        i = 0
        for monster in newmonsterCoords:
            if monster[0] == stateList[0] and monster[1] == stateList[1] and stateList[i+5] == False:
                stateList[3] = False
            i += 1

        newState = tuple(stateList)
        return newState

    def action_cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        monsterStatus = state[5:]
        reached = all(monsterStatus) and state[3]
        return reached

    def h(self, node):
        if self.is_goal(node.state):
            return 0
        else:
            values = []
            coordinates = self.move_monsters(node.state[4])
            i = 0
            for monster in coordinates:
                if node.state[i+5] == False:
                    values.append(abs(monster[0]-node.state[0]))
                i+=1
            return min(values)
        


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

example_state = ('Y', False, False, 1, True, False, False, False)

print(example_route_problem.actions(example_state))
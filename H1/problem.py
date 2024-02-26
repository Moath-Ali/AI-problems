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
            for i in monsterList:
                i[1] = i[1]-1
        elif timestep == 1:
            for i in monsterList:
                i[1] = i[1]-1
        elif timestep == 2:
            for i in monsterList:
                i[1] = i[1]+1
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
        self.monsterCoords = self.move_monsters(mstep)
        stateList[4] = mstep
        #self.state = tuple(stateList)
        if action == 'shoot-arrow':
            if stateList[2] == 'west':
                i = 0
                for monster in self.monsterCoords:
                    for arrow in range(stateList[1],0,-1):
                        if monster[0] == stateList[0] and monster[1] == arrow:
                            stateList[i+5] = True
                    i += 1
            elif stateList[2] == 'east':
                i = 0
                for monster in self.monsterCoords:
                    for arrow in range(stateList[1], self.N+1):
                        if monster[0] == stateList[0] and monster[1] == arrow:
                            stateList[i+5] = True
                    i += 1
            elif stateList[2] == 'north':
                i = 0
                for monster in self.monsterCoords:
                    for arrow in range(stateList[0], self.N+1):
                        if monster[0] == arrow and monster[1] == stateList[1]:
                            stateList[i+5] = True
                    i += 1
            elif stateList[2] == 'south':
                i = 0
                for monster in self.monsterCoords:
                    for arrow in range(stateList[0], 0, -1):
                        if monster[0] == arrow and monster[1] == stateList[1]:
                            stateList[i+5] = True
                    i += 1
            self.state = tuple(stateList)
            newState = tuple(stateList)
            return newState

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
        for monster in self.monsterCoords:
            if monster[0] == stateList[0] and monster[1] == stateList[1] and stateList[i+5] == False:
                stateList[3] = False
            i += 1

        self.state = tuple(stateList)
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
            return min(values)
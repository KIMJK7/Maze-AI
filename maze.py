import sys

class Node():
    def __init__(self, state,parent, action):
        # inclass node we are keeping track of state, parent and action which is taken
        self.state =state
        self.parent= parent
        self.action = action
        
class StakFrontier():
    def __init__(self):
        self.frontier =[]
        
    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier)==0    
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node =self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node 
        
class Queuefrontier(StakFrontier):
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node =self.frontier[0]
            self.frontier = self.frontier[1:]
            return node 
        
class Maze():
    
    def __init__(self,filename):
        
        #read file and set height and weidth of maze
        with open(filename) as f:
            contents=f.read()
            
        #validate start and goal
        if contents.count("A") !=1:   
            raise Exception("maze must have exactly one starting point")
        if contents.count("B") !=1:   
            raise Exception("maze must have exactly one ending point")   
           
        #determine height and width of maze
        contents =contents.splitlines()
        self.height=len(contents)
        self.width= max(len(line) for line in contents)   
        
        #keeping track of walls
        self.walls=[]
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try :
                    if contents[i][j]=="A":
                        self.start=(i,j)
                        row.append(False)
                    elif contents[i][j]=="B":
                        self.goal=(i,j)
                        row.append(False) 
                    elif contents[i][j] ==" ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row) 
        self.solution =None   
        
    def print(self):
        #next line is not complete
        solution= self.solution[1] if self.solution is None else None 
        print()
        for i, row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col :
                    print("🌫️",end="")
                elif(i,j)==self.start:
                    print("A",end="")
                elif(i,j)==self.goal:
                     print("B",end="")
                elif solution is not None and (i,j) in solution:
                    print("*",end="")
                else:
                    print(" ",end="")
            print()
        print()
        
    def neighbors(self,state):
        row,col=state
                
         #all possible actions
        candidates=[
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1)) 
         ]   
        
        #ensure actions are valid
        result=[]
        for action , (r,c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action,(r,c))) 
            except IndexError:
                continue
        return result  
    
    def solve(self):   
        """find a sol to maze , if one exits.""" 
        
        #keep track of number of states explored
        self.num_explored= 0
        
        #initialize frontier to just the starting position
        start= Node(state =self.start, parent=None, action=None)
        frontier=StakFrontier()
        #dept-First search
        frontier.add(start)  
        
        #initialize an empty exploerd set
        self.explored =set()    
        
        #keep looping until solution found
        while True:
            
            #if nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("No solution")
            
            #choose a node from the fronteir
            node = frontier.remove()
            self.num_explored +=1
            
            # if node is the goal, thenwe havea solutio
            if node.state ==self.goal:
                actions =[]
                cells=[]
                #follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node =node.parent
                actions.reverse()
                cells.reverse() 
                self.solution=(actions,cells)
                return   
            #mark node as explored
            self.explored.add(node.state)
            
            #add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child =Node(state=state, parent=None, action=action)
                    frontier.add(child)
                
    def output_image(self,filename,show_soltion=True,show_explored=False):
        from PIL import Image, ImageDraw
        cell_size =50
        cell_border=2
        
        #create a blank canvas
        img=Image.new(
            "RGBA",
            (self.width *cell_size,self.height *cell_border),
            "black"
        )
        draw=ImageDraw.Draw(img)
        solution=self.solution[1] if self.solution is not None else None 
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                
                #walls
                if col:
                    fill=(40,40,40)
                #start    
                elif(i,j)==self.start:
                    fill=(255,0,0)
                #goal
                elif(i,j)==self.goal:
                    fill=(0,171,28)
                #solution
                elif solution is not None and show_soltion and (i,j) in solution:
                    fill=(220,235,113)
                #explored
                elif solution is not None  and show_explored and (i,j) in self.explored:
                    fill=(212,97,85)
                #empty cell
                else: 
                    fill=(237,240,252)
                    
                #draw cell
                draw.rectangle(
                    ([j*cell_size +cell_border ,i*cell_size+cell_border]),
                    ((j+1)*cell_size-cell_border,(i+1)*cell_size-cell_border),
                    fill=fill
                )  
        img.save(filename)  

if len(sys.argv) !=2:
    sys.exit("Usage :python maze.py maze.txt")
    
m=Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving....")
m.solve()
print("solution:")
m.print()
m.output_image("maze.png",show_explored=True)                          
## Kevin Coe         
## kcoe3@gatech.edu  

## Creates an interactive canvas environment. All dots move randomly.
## Clicking yellow dots will make them dissapear.
## Clicking red dots will make them stop moving.


from Tkinter import *
from math import sqrt

#We define a  GUI class that handles drawing the simulated agents
#in the world (on a canvas)
class SimWorld():

    agents = []     #our list of agents...
    running = False #Is the simulation currently running?
    

    #This is the constructor. It draws the window with the canvas.
    def __init__(self, tkMainWin, width =1000, height=1000):
        self.width = width
        self.height = height
        frame = Frame(tkMainWin)
        frame.pack()
        self.canvas = Canvas(frame,width=width,height=height)
        self.canvas.bind("<Button-1>",self.clicked)
        self.canvas.bind("<Button-3>",self.rightClicked)
        self.canvas.pack()
        self.tick()

    def tick(self):
        if self.running:
            print("tick!")
            #Tell each agent to go do something!
            for agent in self.agents:
                agent.action()

            #Schedule the next tick!
            self.canvas.after(300, self.tick)

    #Start the simulation!
    def start(self):
        self.running = True
        self.tick() #Start the tick method!

    #Ask the tick method to stop !
    def stop(self):
        self.running = False

    #This event handler (callback) gets called when the canvas is
    #left clicked. We identify which agent(s) is/are "under" the mouse
    # (current) and call it's clicked method.
    def clicked(self, event):
        items = self.canvas.find_overlapping(event.x-2,event.y-2,
                                             event.x+2, event.y+2)
        for i in items:
            for agent in self.agents :
                if i == agent.iconID:
                    agent.clicked()


    #This handler deals with "right-click" events,
    def rightClicked(self,event):
        print("rightClicked!")
        items = self.canvas.find_overlapping(event.x-2,event.y-2,
                                             event.x+2, event.y+2)
        for i in items:
            for agent in self.agents :
                if i == agent.iconID:
                    agent.rightClicked()


    #When users add an agent to this sim world,
    #we add it to our list of agents, and also tell the
    #agent what world it exists within.
    def addAgent(self, agent ):
        self.agents.append(agent)
        agent.setWorld(self)

    #Allows removal of an agent from the world.
    def removeAgent(self, agent):
        index = self.agents.index(agent)
        self.agents[index].undraw()         
        del self.agents[index]

    #Helper method to calculate eclidian distance
    def distance(self,x1,y1,x2,y2):
        xDiff = (x1-x2) ** 2
        yDiff = (y1-y2) ** 2
        distance = sqrt(xDiff+yDiff)
        return distance
    
    #Given an agent, this method will find the closest OTHER agent.
    #Returns None if their are no other agents.
    def findClosest(self,agent):
        x,y = agent.x, agent.y
        smallest = 9999999999
        closest = None
        for otherAgent in self.agents:
            if agent != otherAgent:
                dist = self.distance(x,y, otherAgent.x, otherAgent.y)
                if dist < smallest:
                    closest = otherAgent
                    smallest = dist
        return closest
    
    
        
        
        



#Here we define a generic "Agent" class. Generic agents move randomly.      
class Agent:
    x = 0
    y = 0
    speed = 5
    world = None
    color = ""
    iconID = None
    
    def __init__(self, X=0, Y=0):
       self.x = X
       self.y = Y

    #This method is called when the agent is added to a SimWorld.  
    def setWorld(self,world):
       self.world = world
       self.draw()

    #Agents know how to draw themselves on a worlds canvas.
    def draw(self):
        bbox = (self.x-2,self.y-2,self.x+2,self.y+2)
        self.iconID = self.world.canvas.create_oval( bbox, fill=self.color)

    #Agents can also undraw themselves if needed.
    def undraw(self):
        self.world.canvas.delete(self.iconID)
        

    def moveIcon(self,x,y):
        self.world.canvas.move(self.iconID,x,y)

    def randomMove(self,distance):
        from random import randrange
        xDelta = randrange(-distance,distance+1)
        yDelta = randrange(-distance, distance+1)

        #Don't move outside the world!
        if self.x +xDelta < 0:
            xDelta = -xDelta
        if self.y +yDelta < 0:
            yDelta = -yDelta

        if self.x +xDelta > self.world.width:
            xDelta = -xDelta
        if self.y +yDelta > self.world.height:
            yDelta = -yDelta
        
        self.moveIcon(xDelta,yDelta)
        self.x = self.x + xDelta
        self.y = self.y + yDelta

    #Every "tick" of the clock the world tells Agents to take their action
    #by calling this method.
    def action(self):
        #By default, agents move randomly...
        self.randomMove(self.speed)

    #If the user (left) clicks on this agent, the following method will be called
    def clicked(self):
        print("I was clicked!")

    #If the user (right) clicks on this agent, the following method will be called
    def rightClicked(self):
        print("I was rightClicked!")



class YellowAgent(Agent):
    color="yellow"

    #Yellow agents will disapear if you click them.
    def clicked(self):
        self.world.removeAgent(self)

class OrangeAgent(Agent):
    color = "orange"
    speed = 10

    #Orange agents will stop if you click them.
    def clicked(self):
        self.speed = 0
    
    
#If this code is ran directly, demo some agents:
if __name__ == "__main__":
   #This code starts up TK and creates a main window.
   mainWin = Tk()

   #This code creates an instance of the TTT object.
   sw = SimWorld( mainWin)
   for i in range(10):
      sw.addAgent( OrangeAgent(30,30) )
      sw.addAgent(YellowAgent(10,10) )
   sw.start()
   #This line starts the main event handling loop and sets us on our way...
   mainWin.mainloop()

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from random import randrange
import math


class Agent(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.speed = 1

    #compute the local density for k-nearest neighbours
    def k_local_density(self, k):
        r=1
        while(1):
            neighbours = self.model.grid.get_neighbors(self.pos,True,False,r)
            if len(neighbours) < k:
                r+=1
            else:
                break
        density = k/(math.pi * pow(r,2))
        return density



    def step(self):

        oxy_level = self.model.get_oxygen(self.pos[0],self.pos[1])
        c,d,oxy_grad = self.model.get_oxy_grad(self.pos[0],self.pos[1])
        a=int(c)
        b=int(d)
        try:
            if not self.model.grid.out_of_bounds((self.pos[0]+a,self.pos[1]+b)):
                if oxy_level <5:
                    self.model.grid.move_agent(self,(self.pos[0]+a,self.pos[1]+b))
            if not self.model.grid.out_of_bounds((self.pos[0]-a,self.pos[1]-b)):
                if oxy_level >12:
                    self.model.grid.move_agent(self,(self.pos[0]-a,self.pos[1]-b))
            if self.pos == (self.model.width/2,self.model.height/2):
                self.model.grid.move_agent(self,(self.pos[0]-1,self.pos[1]-1))
        except:
            try:
                n=1
                if oxy_level <5:
                    while(1):
                        if self.model.grid.is_cell_empty((self.pos[0]+(a*n),self.pos[1]+(b*n))):
                            for m in range(n):
                                self.model.grid.move_agent(self.model.grid[self.pos[0]+(a*(n-1-m))][self.pos[1]+(a*(n-1-m))],(self.pos[0]+(a*(n-m)),self.pos[1]+(a*(n-m))))
                            break
                        else:
                            n+=1
                n=1
                if oxy_level >12:
                    while(1):
                        if self.model.grid.is_cell_empty((self.pos[0]-(a*n),self.pos[1]-(b*n))):
                            for m in range(n):
                                self.model.grid.move_agent(self.model.grid[self.pos[0]-(a*(n-m-1))][self.pos[1]-(a*(n-m-1))],(self.pos[0]-(a*(n-m)),self.pos[1]-a*(n-m)))
                            break
                        else:
                            n+=1
            except:
                self.model.grid.move_agent(self,self.pos)


class Model(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height, width, a_density=0.1, f_density = 0.1):
        """
        """

        self.height = height
        self.width = width
        self.a_density = a_density
        self.f_density = f_density

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=False)
        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)

        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.a_density:
                agent = Agent((x, y), self)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)


    def get_oxygen(self,x,y):
        x1 = self.width
        y1 = self.height
        return -1*pow((x/(x1/10))-(x1/10),2) -pow((y/(y1/10))-(y1/10),2) +(x1+y1)/4
    def get_oxy_grad(self, x, y):
        a = -(((2*x)/(pow(self.width,2)/100)) -2)
        b = -(((2*y)/(pow(self.height,2)/100)) -2)
        if  abs(b) != 0:
            b = b / abs(b)
        if abs(a) != 0:
            a = a / abs(a)

        total = -1*a - b
        return a,b,total

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

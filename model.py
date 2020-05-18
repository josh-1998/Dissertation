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
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 1
        self.direction = 1


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

    def kslow(self,kso,ks,density):
        return kso + ks * Density

    def r_rev(self,r_,density):
        r_rev = r_*density
        return r_rev


    def m_vector(self):
        v = [0,0]
        u = 0
        r=1
        while(1):
            neighbors = self.model.grid.get_neighbors(self.pos,True,False,r)
            if len(neighbors) < 5:
                r+=1
            else:
                break
        for neighbour in self.model.grid.iter_neighbors(self.pos,True,False,r):
            v[0] = v[0] + (neighbour.pos[0] - self.pos[0])
            v[1] = v[1] + (neighbour.pos[1] - self.pos[1])
        try:
            u = math.sqrt(pow(v[0],2) + pow(v[1],2))
            v[0] = v[0]/u
            v[1] = v[1]/u
            return v
        except:
            return [0,0]



    def step(self):
        self.direction = 1
        p = self.k_local_density(6)
        r_r = self.r_rev(self.model.r_,p)
        print(r_r)
        if r_r > 0.1:
            self.direction = self.direction * -1
        m = self.m_vector()
        self.x = self.x + (self.direction * self.speed * m[0])
        self.y = self.y + (self.direction * self.speed * m[1])
        try:
            self.model.grid.move_agent(self,(round(self.x),round(self.y)))
        except:
            self.model.grid.move_agent(self,(self.pos[0],self.pos[1]))



class Model(Model):

    def __init__(self, height, width, a_density=0.1, r_=0.1, k_=0.1):

        self.height = height
        self.width = width
        self.a_density = a_density
        self.r_ = r_
        self.k_ = k_

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


    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

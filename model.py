from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import random
from random import randrange
import math


class Agent(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 2
        self.direction = 1
        self.roaming = 0


    #compute the local density for k-nearest neighbours
    def k_local_density(self, k):
        r=1
        while(r<7):
            neighbours = self.model.grid.get_neighbors(self.pos,True,False,r)
            if len(neighbours) < k:
                r+=1
            else:
                break
        if len(neighbours) == 0 or self.model.food_matrix[self.pos[0]][self.pos[1]] == 0:
            self.roaming = 1
        else:
            self.roaming = 0
        density = k/(math.pi * pow(r,2))
        return density

    def kslow(self,kso,k,density):
        return kso + (k * density)

    def kfast(self,kfo,k,density):
        return kfo * math.exp(-k * density)

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
        self.model.food_matrix[self.pos[0]][self.pos[1]] = self.model.food_matrix[self.pos[0]][self.pos[1]] - 5
        self.direction = 1
        p = self.k_local_density(6)
        r_r = self.r_rev(self.model.r_,p)
        kslow = self.kslow(0.01,self.model.k_,p)
        kfast = self.kfast(1.8,self.model.k_,p)
        m = self.m_vector()
        if self.model.food_matrix[self.pos[0]][self.pos[1]] <= 0:
            self.speed = 2
            self.direction = -1
        else:
            if r_r > 0.1:
                self.direction = self.direction * -1
            if kslow > 0.1 and self.speed == 2:
                self.speed = 0.5
            if kfast > 1.63 and self.speed ==0.5:
                self.speed = 2
        try:
            if self.roaming == 1:
                a = round(randrange(3)-1)
                b = round(randrange(3)-1)
                if not self.model.grid.out_of_bounds((self.pos[0]+a,self.pos[1]+b)):
                    self.model.grid.move_agent(self,(self.pos[0]+a,self.pos[1]+b))
            else:
                self.x = self.x + (self.direction * self.speed * m[0])
                self.y = self.y + (self.direction * self.speed * m[1])

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

        random.seed(9001)
        n = self.height
        m = self.width
        self.food_matrix = [[100] * m for i in range(n)]
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            a = random.random()
            if a < self.a_density:
                agent = Agent((x, y), self)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)


    def step(self):

        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

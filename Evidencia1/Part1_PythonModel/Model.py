# Alejandro Díaz Villagómez - A01276769
# Fecha - 18/Noviembre/2022
# Simulación de una intersección

from mesa import Model
from random import randint
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa import batch_run
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from Agents import *

# Calculamos los movimientos totales de todos los agentes
def show_agent_moves(model):
    tot_steps = []
    for a in model.schedule.agents:
        if a.unique_id < 6:
            tot_steps.append(a.personal_steps)
    return sum(tot_steps)


# MODELO
class OrderingRobotsModel(Model):
    def __init__(self, N, width, height):
        self.steps = 0
        self.num_cells = width * height
        self.num_agents = N
        self.shelf_coord = []
        self.stack_box_coord = [(1, 1), (11, 1), (1, 11), (11, 11)]
        self.ordered_box_percentage = 0

        # Espacio físico para los agentes
        # No permitimos que se salgan del mapa
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Creamos una lista con coordenadas únicas para las "x" - apilamiento de cajas
        for i in range(len(self.stack_box_coord)):
            sb = StackBox(i + 50, self)
            self.schedule.add(sb)
            self.grid.place_agent(sb, self.stack_box_coord[i])

        # Creamos una lista con coordenadas únicas para los estantes
        for i in range (2, 11):
            # shelf_coord.append((3, i))
            # shelf_coord.append((9, i))
            self.shelf_coord.append((i, 3))
            self.shelf_coord.append((i, 9))
        
        # Creamos una lista con coordenadas únicas para las cajas
        box_coord = []
        k = randint(8, 20)
        while len(box_coord) < k:
            box_pos = (randint(0, height - 1), randint(0, width - 1))
            if box_pos not in self.shelf_coord and box_pos not in self.stack_box_coord and box_pos not in box_coord:
                box_coord.append(box_pos)
        
        # Creamos una lista con coordenadas únicas para los robots
        robot_coord = []
        while len(robot_coord) < self.num_agents:
            robot_pos = (randint(0, height - 1), randint(0, width - 1))
            if robot_pos not in self.shelf_coord and robot_pos not in self.stack_box_coord and robot_pos not in box_coord and robot_pos not in robot_coord:
                robot_coord.append(robot_pos)
        

        # Agregamos los agentes al mapa
        x = j = z = 0
        for i in range(1, self.num_agents + len(self.shelf_coord) + k + 1):
            if i <= self.num_agents:
                r = Robot(i, self)
                self.schedule.add(r)
                self.grid.place_agent(r, robot_coord[x])
                x += 1
            elif i > self.num_agents and i <= self.num_agents + len(self.shelf_coord):
                s = Shelf(100 + j, self)
                self.schedule.add(s)
                self.grid.place_agent(s, self.shelf_coord[j])
                j += 1
            else:
                b = Box(10 + z, self)
                self.schedule.add(b)
                self.grid.place_agent(b, box_coord[z])
                z += 1
        


        # Metrics we will measure about our model
        self.datacollector = DataCollector(
            model_reporters={
                "Movimientos_Agentes": show_agent_moves,
            },
        )

    # ¿Qué pasará en cada unidad de tiempo?
    def step(self):
        # Corre 1 tick en el reloj de nuestra simulación
        self.steps += 1
        self.datacollector.collect(self)
        self.schedule.step()
        # self.box_percentage += 1

        if self.ordered_box_percentage >= 25:
            self.running = False
    
    #Debemos checar el porcentaje de cajas ordenadas (25%)
    def run_model(self):
        while self.running:
            self.step()


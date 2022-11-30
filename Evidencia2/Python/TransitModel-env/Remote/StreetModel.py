# Alejandro Díaz Villagómez - A01276769
# Emiliano Saucedo Arriola - A01659258
# Alfonso Pineda Cedillo - A01660394
# Fecha - 30/Noviembre/2022
# Evidencia 2 - Simulación de una intersección

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from Agents import *


class StreetModel(Model):
    def __init__(self, N=10, width=21, height=21, collisions=False):
        self.num_agents = N
        self.running = True
        self.neighbors = False
        self.accident = False
        self.tot_crashes = 0
        self.counting_cars = 0
        self.steps = 0
        self.max_waiting_time = 0
        self.mean_waiting_time = 0
        self.max_mean_waiting_time = 0
        self.accept_collisions = collisions

        # Espacio físico para los agentes
        # Permitimos que se salgan del mapa
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Colocamos los carros
        coord_traffic = [(7, 9), (13, 10), (10, 7), (9, 13)]
        coord_cars = [(9, 15), (18, 10), (10, 2), (0, 9), (9, 5),
                      (2, 9), (19, 0), (2, 20), (15, 20), (11, 18)]
        coord_cars_dir = [4, 2, 3, 1, 4, 1, 2, 1, 1, 3]
        for j in range(0, len(coord_cars)):
            car = Car(j + len(coord_traffic) + 1, self, coord_cars_dir[j])
            self.schedule.add(car)
            self.grid.place_agent(car, coord_cars[j])

        # Le damos color al grid
        id_cont = 1
        for i in range(width):
            for j in range(height):
                # Es una celda calle (sus IDs serán mayor a 1000)
                if (i > 7 and i < 13) or (j > 7 and j < 13):
                    id = 1000 + id_cont
                    a = Color(id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (i, j))
                # Es una celda pasto (sus IDs serán mayor a 2000)
                else:
                    id = 2000 + id_cont
                    a = Color(id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (i, j))
                id_cont += 1

        # Colocamos los semáforos
        print("LEN")
        print(len(self.schedule.agents))
        # coord_traffic = [(7, 9)]
        for i in range(0, len(coord_traffic)):
            traffic_light = TrafficLight(i + 1, self, 0)
            self.schedule.add(traffic_light)
            self.grid.place_agent(traffic_light, coord_traffic[i])

        # Carros para ejemplo de "colisión"
        # c15 = Car(15, self, 4)
        # self.schedule.add(c15)
        # self.grid.place_agent(c15, (9, 13))
        # c25 = Car(25, self, 2)
        # self.schedule.add(c25)
        # self.grid.place_agent(c25, (11, 11))

    def trafficLightIsActive(self):
        for agent in self.schedule.agents:
            if agent.unique_id < 5 and agent.pass_car == True:
                return True
        return False

    def get_mean_max_waiting_time(self):
        tot_cars = tot_waiting = 0
        for agent in self.schedule.agents:
            if agent.unique_id > 4 and agent.unique_id < 50 and agent.waiting > self.max_waiting_time:
                self.max_waiting_time = agent.waiting

            if agent.unique_id > 4 and agent.unique_id < 50:
                tot_cars += 1
                tot_waiting += agent.waiting
        self.mean_waiting_time = int(tot_waiting/tot_cars)
        if self.mean_waiting_time > self.max_mean_waiting_time:
            self.max_mean_waiting_time = self.mean_waiting_time

    def step(self):
        self.steps += 1
        self.get_mean_max_waiting_time()
        # self.datacollector.collect(self)
        self.schedule.step()

        positions = []
        for i in range(self.num_agents):
            vehicle_id = self.schedule.agents[i].unique_id
            xy = self.schedule.agents[i].pos
            p = [
                vehicle_id,
                 xy[0],
                 2.35,
                 xy[1]
                ]
            positions.append(p)
        print(positions)

        lights = []
        for i in range(451, 455):
            light_id = self.schedule.agents[i].unique_id
            state = self.schedule.agents[i].state

            s = [
                light_id,
                 state
                 ]

            lights.append(s)
        print(lights)

        if self.accident:
            self.tot_crashes += 0.5
            self.accident = False

        if self.steps >= 300:
            print("\nMax Time", self.max_waiting_time)
            print("Total Cars", self.counting_cars)
            print("Car Crashes", int(self.tot_crashes/2))
            self.running = False

        return positions, lights
        
    def run_model(self):
        while self.running:
            self.step()


# Parámetros para correr el modelo varias veces
model_params = {"N": 6, "width": 21, "height": 21, "collisions": True}
# Integrantes:
    # Alejandro Díaz Villagómez - A01276769
    # Emiliano Saucedo Arriola - A01659258
    # Alfonso Pineda Cedillo - A01660394

import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import random

from Agents import *

# Calculamos los movimientos totales de todos los agentes
def show_agent_moves(model):
    tot_steps = []
    for a in model.schedule.agents:
        if a.unique_id < 6:
            tot_steps.append(a.personal_steps)
    return sum(tot_steps)

# Cajas ordenadas por agente
def show_agent_boxes(model):
    tot_boxes = []
    for a in model.schedule.agents:
        if a.unique_id < 6:
            tot_boxes.append(a.boxes_delivered)
    return tot_boxes

# Cajas ordenadas
def show_agent_ordered_boxes(model): 
    tot_boxes = []
    for a in model.schedule.agents:
        if a.unique_id < 6:
            tot_boxes.append(a.boxes_delivered)
    return sum(tot_boxes)

def show_unordered_boxes(model):
    return model.unordered_boxes


# MODELO
class OrderingRobotsModel(mesa.Model):
    def __init__(self, N, width, height):
        self.steps = 0
        self.num_agents = N
        self.shelf_coord = []
        self.stack_box_coord = [(1, 1), (11, 1), (1, 11), (11, 11)]
        self.unordered_boxes = 0

        # Espacio físico para los agentes
        # No permitimos que se salgan del mapa
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        # Creamos una lista con coordenadas únicas para las "x" - apilamiento de cajas
        for i in range(len(self.stack_box_coord)):
            sb = StackBox(i + 50, self)
            self.schedule.add(sb)
            self.grid.place_agent(sb, self.stack_box_coord[i])

        # Creamos una lista con coordenadas únicas para los estantes
        for i in range (2, 11):
            if i == 4 or i == 8:
                pass
            else:
                self.shelf_coord.append((i, 3))
                self.shelf_coord.append((i, 6))
                self.shelf_coord.append((i, 9))
        
        # Creamos una lista con coordenadas únicas para las cajas
        box_coord = []
        k = random.randint(8, 20)
        self.unordered_boxes = self.total_boxes = k
        print("Boxes: " + str(k))
        while len(box_coord) < k:
            box_pos = (random.randint(0, height - 1), random.randint(0, width - 1))
            if box_pos not in self.shelf_coord and box_pos not in self.stack_box_coord and box_pos not in box_coord:
                box_coord.append(box_pos)
        
        # Creamos una lista con coordenadas únicas para los robots
        robot_coord = []
        while len(robot_coord) < self.num_agents:
            robot_pos = (random.randint(0, height - 1), random.randint(0, width - 1))
            if robot_pos not in self.shelf_coord and robot_pos not in self.stack_box_coord and robot_pos not in box_coord and robot_pos not in robot_coord:
                robot_coord.append(robot_pos)
        

        # Agregamos los agentes al mapa
        x = j = z = 0
        # Robots: 0 - 5
        for i in range(1, self.num_agents + len(self.shelf_coord) + k + 1):
            if i <= self.num_agents:
                r = Robot(i, self)
                self.schedule.add(r)
                self.grid.place_agent(r, robot_coord[x])
                x += 1
            # Estantes: 6 - 13
            elif i > self.num_agents and i <= self.num_agents + len(self.shelf_coord):
                s = Shelf(100 + j, self)
                self.schedule.add(s)
                self.grid.place_agent(s, self.shelf_coord[j])
                j += 1
            # Cajas: 14 - 33
            else:
                b = Box(10 + z, self)
                self.schedule.add(b)
                self.grid.place_agent(b, box_coord[z])
                z += 1
        


        # Metrics we will measure about our model
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Movimientos_Agentes": show_agent_moves,
                "Cajas_Ordenadas": show_agent_ordered_boxes,
                "Cajas_Desordenadas": show_unordered_boxes,
                "Robot1": lambda m: show_agent_boxes(m)[0],
                "Robot2": lambda m: show_agent_boxes(m)[1],
                "Robot3": lambda m: show_agent_boxes(m)[2],
                "Robot4": lambda m: show_agent_boxes(m)[3],
                "Robot5": lambda m: show_agent_boxes(m)[4],
            },
        )

    # ¿Qué pasará en cada unidad de tiempo?
    def step(self):
        # Corre 1 tick en el reloj de nuestra simulación
        self.steps += 1
        self.datacollector.collect(self)
        self.schedule.step()
        
        # ebemos checar el porcentaje de cajas ordenadas (25%)
        self.percentage = show_agent_ordered_boxes(self) * 100 / self.total_boxes
        print("Total de cajas al inicio: " + str (self.total_boxes))
        print("Ordenados: "  + str (show_agent_ordered_boxes(self)))
        print("Desordenados: "  + str (show_unordered_boxes(self)))
        print("Porcentaje ordenado: " + str(self.percentage))
        if self.percentage >= 75:
            self.running = False
    
    def run_model(self):
        while self.running:
            self.step()


# Parámetros para correr el modelo varias veces
model_params = {
    "N": 5,
    "width": 13,
    "height": 13
}

# Usaremos batch_run
results = mesa.batch_run(
    OrderingRobotsModel,
    parameters=model_params,
    iterations=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=False,
)

# Convertimos los resultados en un DataFrame
results_df = pd.DataFrame(results)
print(results_df.keys())

# Agrupamos la información y obtenemos solo los últimos valores
grouped_iterations = pd.DataFrame(
    columns=['iteration', 'Step', 'Movimientos_Agentes', 'Cajas_Ordenadas', 'Cajas_Desordenadas'])

for it, group in results_df.groupby(["iteration"]):
    grouped_iterations = grouped_iterations.append(
        {'iteration': group.iloc[-1].iteration,
         'Step': group.iloc[-1].Step,
         'Movimientos_Agentes': group.iloc[-1].Movimientos_Agentes,
         'Cajas_Ordenadas': group.iloc[-1].Cajas_Ordenadas,
         'Cajas_Desordenadas': group.iloc[-1].Cajas_Desordenadas},
        ignore_index=True)
#print(grouped_iterations.to_string(index=False, max_rows=25))
print(grouped_iterations.to_string(index=False))

# Hacemos una gráfica que representa el tiempo necesario para ordenar el 25% de
# de las cajas en las 100 iteraciones
# El grid es de 10x10 (100 celdas) y el tiempo máximo es de 50 pasos
sns.set_theme()
sns.scatterplot(
    data=grouped_iterations,
    x="iteration", y="Step",
)
plt.title('Tiempo para apilar las cajas (75%)')
plt.xlabel('Iteraciones')
plt.ylabel('Steps')
plt.show()

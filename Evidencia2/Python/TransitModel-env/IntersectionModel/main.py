# Alejandro Díaz Villagómez - A01276769
# Emiliano Saucedo Arriola - A01659258
# Alfonso Pineda Cedillo - A01660394
# Fecha - 29/Noviembre/2022
# Evidencia 2 - Simulación de una intersección

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

#from CleaningModel import CleaningModel
from StreetModel import *

bool_colls = False

while True:
    colls = str(input("¿Quieres considerar choques? (y/n): "))
    if colls == "y":
        bool_colls = True
        break

    elif colls == "n":
        break


def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0
    }
    # Calle
    if agent.unique_id > 1000 and agent.unique_id < 2000:
        portrayal["Color"] = "grey"

    # Pasto
    elif agent.unique_id > 2000:
        portrayal["Color"] = "green"

    # Semáforos
    elif agent.unique_id < 5:
        if agent.state == 0:
            portrayal["Color"] = "red"
        if agent.state == 1:
            portrayal["Color"] = "yellow"
        if agent.state == 2:
            portrayal["Color"] = "green"

    # Carros
    else:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.8
        portrayal["Color"] = "black"

    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    21,
    21,
    600,
    600
)

# Contador de coches que pasan
chart_counting_cars = ChartModule([{
    'Label': 'Counting_Cars',
    'Color': 'Black'}],
    data_collector_name='datacollector',
    canvas_height=40,
    canvas_width=80)

# Accidentes reportados
chart_car_crashes = ChartModule([{
    'Label': 'Car_Crashes',
    'Color': 'Black'}],
    data_collector_name='datacollector',
    canvas_height=40,
    canvas_width=80)

# Tiempo máximo de espera
chart_max_time = ChartModule([{
    'Label': 'Max_Waiting_Time',
    'Color': 'Black'}],
    data_collector_name='datacollector',
    canvas_height=40,
    canvas_width=80)

# Inicializamos el Modelo
#model_params = {"N": 4, "width": 21, "height": 21}
model_params = {"N": 6, "width": 21, "height": 21, "collisions": bool_colls}

# Elementos que se mostrarán en el servidor
server = ModularServer(
    StreetModel,
    [grid, chart_counting_cars, chart_car_crashes, chart_max_time],
    "Intersection Model",
    model_params
)

server.port = 8521
server.launch()
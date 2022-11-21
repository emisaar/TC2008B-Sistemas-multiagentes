# Alejandro Díaz Villagómez - A01276769

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, PieChartModule, CanvasGrid

from Model import *

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0
    }

    if agent.unique_id <= 5:
        portrayal["Shape"] = "Robot_pic.png"
        portrayal["r"] = 1,
    elif agent.unique_id >= 50 and agent.unique_id < 90:
        # portrayal["Shape"] = "Shelf.png"
        portrayal["Shape"] = "x.png"
        portrayal["r"] = 0.2
    elif agent.unique_id >= 100:
        # portrayal["Shape"] = "Shelf.png"
        portrayal["Shape"] = "s2.jpg"
        portrayal["r"] = 0.2
    else:
        portrayal["Shape"] = "Box.png"
        portrayal["r"] = 0.2

    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    13,
    13,
    600,
    600
)


# Movimientos de los agentes
chart_agents_moves = ChartModule([{
    'Label': 'Movimientos_Agentes',
    'Color': 'Black'}],
    data_collector_name='datacollector',
    canvas_height=40,
    canvas_width=80)

# Cajas ordenadas vs cajas desordenadas (%)
chart_ordered_boxes = PieChartModule([
    {'Label': 'Cajas_Ordenadas', 'Color': 'Green'},
    {'Label': 'Cajas_Desordenadas', 'Color': 'Red'}],
    data_collector_name='datacollector',
    canvas_height=500,
    canvas_width=500)


# Inicializamos el Modelo
model_params = {"N": 5, "width": 13, "height": 13}

# Elementos que se mostrarán en el servidor
server = ModularServer(
    OrderingRobotsModel,
    [grid, chart_agents_moves, chart_ordered_boxes],
    "Ordering-Robots Model",
    model_params
)

server.port = 8521
server.launch()

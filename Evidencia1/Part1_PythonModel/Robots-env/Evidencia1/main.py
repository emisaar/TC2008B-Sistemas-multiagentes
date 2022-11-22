# Integrantes:
    # Alejandro Díaz Villagómez - A01276769
    # Emiliano Saucedo Arriola - A01659258
    # Alfonso Pineda Cedillo - A01660394

# Fecha: 22/11/2022
# Actividad Integradora 1 - Parte 1
# Modelado computacional de un sistema de Robots en un Almacén

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, PieChartModule, CanvasGrid

from Portrayal import agent_portrayal
from Model import *


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

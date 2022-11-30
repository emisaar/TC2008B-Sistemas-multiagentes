# Alejandro Díaz Villagómez - A01276769
# Emiliano Saucedo Arriola - A01659258
# Alfonso Pineda Cedillo - A01660394
# Fecha - 29/Noviembre/2022
# Evidencia 2 - Simulación de una intersección - dummy

from random import randint, seed
from mesa import Agent

# Semilla para generar números aleatorios
seed(1)


# Calculamos la cantidad de choques en el modelo
def compute_car_crashes(model):
    return int(model.tot_crashes/2)


# Calculamos la cantidad de carros que pasan por los semáforos
def compute_counting_cars(model):
    return model.counting_cars


# Calculamos el tiempo máximo de espera de un coche
def compute_max_waiting_time(model):
    return model.max_waiting_time


# Calculamos el tiempo promedio de espera de los coches
def compute_mean_waiting_time(model):
    return model.mean_waiting_time


# Calculamos el tiempo promedio máximo de espera (por ejecución)
def compute_simulation_mean_waiting_time(model):
    return model.max_mean_waiting_time


# Usaremos este agente para colorear el grid
class Color(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


# Agente 1 - Carros
class Car(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.moving = True
        self.mov_dir = direction
        self.waiting = 0

    # ¿Qué pasará en cada unidad de tiempo?
    def step(self):
        if self.moving == True:
            self.move()

    # Función para movernos
    def move(self):
        x, y = self.pos
        num = randint(0, 1)
        # Hay 4 posibles direcciones: derecha(1), izquierda(2), arriba(3), abajo(4)
        # Si llegan al límite del grid, rotamos su dirección 90º
        if self.mov_dir == 1:
            if x + 1 >= 21:
                new_position = (x, y - 1)
                self.mov_dir = 4
            elif y == 20 and x == 9 and num == 1:
                new_position = (x, y - 1)
                self.mov_dir = 4
            else:
                new_position = (x + 1, y)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
        elif self.mov_dir == 2:
            if x - 1 < 0:
                new_position = (x, y + 1)
                self.mov_dir = 3
            elif y == 0 and x == 10 and num == 1:
                new_position = (x, y + 1)
                self.mov_dir = 3
            else:
                new_position = (x - 1, y)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
        elif self.mov_dir == 3:
            if y + 1 >= 21:
                new_position = (x + 1, y)
                self.mov_dir = 1
            elif x == 0 and y == 9 and num == 1:
                new_position = (x + 1, y)
                self.mov_dir = 1
            else:
                new_position = (x, y + 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
        elif self.mov_dir == 4:
            if y - 1 < 0:
                new_position = (x - 1, y)
                self.mov_dir = 2
            elif x == 20 and y == 10 and num == 1:
                new_position = (x - 1, y)
                self.mov_dir = 2
            else:
                new_position = (x, y - 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])

        if len(cellmates) > 1:
            for c in cellmates:
                # El semáforo vecino está en rojo - no se puede pasar
                if c.unique_id < 5 and c.pass_car == False:
                    self.waiting += 1

                # El semáforo está en verde o amarillo - puedo pasar
                elif c.unique_id < 5 and c.pass_car == True:
                    self.waiting = 0
                    self.model.grid.move_agent(self, new_position)
                    self.model.counting_cars += 1

                elif self.model.accept_collisions and c.unique_id > 4 and c.unique_id < 100:
                    self.model.grid.move_agent(self, new_position)

        # No hay semáforo, el coche puede avanzar
        else:
            self.model.grid.move_agent(self, new_position)

        # Hay un choque ?
        if self.model.accept_collisions:
            list_a = []
            for a in self.model.schedule.agents:
                if a.unique_id > 4 and a.unique_id < 100:
                    list_a.append(a.pos)
            noRepeatingElements = set(list_a)

            # Hubo un choque, es necesario reportarlo
            if len(noRepeatingElements) != len(list_a):
                self.model.accident = True


# Agente 2 - Semáforos
class TrafficLight(Agent):
    def __init__(self, unique_id, model, color):
        super().__init__(unique_id, model)
        # Hay tres estados: rojo(0), amarillo(1) y verde(2)
        self.state = color
        self.pass_car = False

    def reset_traffic_light(self):
        self.state = 0
        self.pass_car = False

    def step(self):
        if self.model.steps % 5 == 0:
            self.reset_traffic_light()

            if self.model.id_traffic == self.unique_id:
                self.state = 2
                self.pass_car = True

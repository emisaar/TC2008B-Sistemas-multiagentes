# Alejandro Díaz Villagómez - A01276769
# Emiliano Saucedo Arriola - A01659258
# Alfonso Pineda Cedillo - A01660394
# Fecha - 29/Noviembre/2022
# Evidencia 2 - Simulación de una intersección

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
            elif y == 0 and x == 11 and num == 1:
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
            elif x == 20 and y == 11 and num == 1:
                new_position = (x - 1, y)
                self.mov_dir = 2
            else:
                new_position = (x, y - 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])

        if len(cellmates) > 1:
            for c in cellmates:
                # El semáforo vecino está en rojo - no hay semáforo activo
                if c.unique_id < 5 and c.pass_car == False and c.waiting_time <= 0 and not self.model.trafficLightIsActive():
                    self.waiting = 0
                    c.change_traffic_light(0)

                # Sigue activo el semáforo
                elif c.unique_id < 5 and c.pass_car == True and c.waiting_time > 0:
                    self.waiting = 0
                    c.change_traffic_light(1)
                    self.model.grid.move_agent(self, new_position)
                    self.model.counting_cars += 1

                # El semáforo vecino está en rojo - hay semáforo activo
                elif c.unique_id < 5 and c.pass_car == False and c.waiting_time <= 0 and self.model.trafficLightIsActive():
                    self.waiting += 1
                    c.change_traffic_light(2)

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
        self.waiting_time = 0

    def change_traffic_light(self, case):
        # El semáforo está en rojo, hay que checar el estado de los demás semáforos
        if case == 0:
            self.state = 2
            self.waiting_time = 6
            self.pass_car = True

        # El semáforo está en amarillo y no se ha acabado el tiempo (Verde)
        elif case == 1:
            self.state = 1

        # El semáforo vecino está en rojo - hay semáforo activo
        elif case == 2:
            pass

    def step(self):
        if self.waiting_time > 0:
            self.waiting_time -= 1
        if self.waiting_time == 0:
            self.pass_car = False
            self.state = 0

# Alejandro Díaz Villagómez - A01276769

# Fecha - 21/Noviembre/2022
# Evidencia 1

from mesa import Agent

# AGENTES
#Estantes - unique_id > 100
class Shelf(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

#Cajas - unique_id [10-30]
class Box(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

#Pilas de cajas - unique_id [50-53]
class StackBox(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isFull = False
        self.box_counting = 0
    

#Cajas - unique_id [1-5]
class Robot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.personal_steps = 0
        self.hasBox = False

    # ¿Qué pasará en cada unidad de tiempo?
    def step(self):
        #Si no tenemos una caja y la celda actual no es una caja, nos movemos de manera random
        if self.hasBox == False and self.order_box() == False:
            self.moveRandom()
        #Si recogemos una caja, no nos movemos 1 step
        if self.order_box():
            pass
        #Si tenemos una caja, no podemos cargar más. Nos movemos a una pila
        if self.hasBox:
            self.move2Stack()

    # Buscamos los movimientos posibles de manera aleatoria
    def moveRandom(self):
        possible_steps = self.model.grid.get_neighborhood(
            # Posición actual
            self.pos,
            # Vecinos en diagonal
            moore=False,
            # Puede que un agente no se mueva
            #include_center=True
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        #La nueva posición es un estante, cambiamos rumbo
        if new_position in self.model.shelf_coord:
            possible_steps.remove(new_position)
            new_position = self.random.choice(possible_steps)

        # Checamos que la nueva posición no coincida con ningún otro robot
        cellmates = self.model.grid.get_cell_list_contents([new_position])
        if len(cellmates) > 0:
            for c in cellmates:
                if c.unique_id < 6:
                    self.model.grid.move_agent(self, self.pos)
                    return
        # Si nos podemos mover, aumentamos el conteo de movimientos del agente
        self.personal_steps += 1
        self.model.grid.move_agent(self, new_position)
    
    def move2Stack(self):
        #Si el robot está cargando una caja, debe encontrar la pila más cercana disponible,
        #para ello, determinamos la pos actual del robot y el estado de cada pila
        #Es necesario calcular en cada step estos elementos por si se llenan las pilas
        print(self.pos)
        x, y = self.pos
        available_stacks = []
        for agent in self.model.schedule.agents:
            if agent.unique_id >= 50 and agent.unique_id <= 53 and agent.isFull == False:
                available_stacks.append(agent.pos)
        
        #Calculamos las distancias del robot a las pilas
        minDist = 1000
        for i in range(len(available_stacks)):
            dist = math.dist(self.pos, available_stacks[i])
            if dist < minDist:


    # Función para recoger las cajas
    def order_box(self):
        # Recoge la caja en la celda en la que estoy (si actualmente no estoy cargando una)
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 0:
            for c in cellmates:
                if c.unique_id > 5 and c.unique_id < 40 and self.hasBox == False:
                    self.model.grid.remove_agent(c)
                    self.hasBox = True
                    return True
        return False
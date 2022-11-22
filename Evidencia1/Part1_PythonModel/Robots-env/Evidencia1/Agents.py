# Integrantes:
    # Alejandro Díaz Villagómez - A01276769
    # Emiliano Saucedo Arriola - A01659258
    # Alfonso Pineda Cedillo - A01660394
    
import math
import mesa

# AGENTES
#Estantes - unique_id > 100
class Shelf(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

#Cajas - unique_id [10-30]
class Box(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

#Pilas de cajas - unique_id [50-53]
class StackBox(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isFull = False
        self.box_counting = 0
    

#Cajas - unique_id [1-5]
class Robot(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.personal_steps = 0
        self.hasBox = False
        self.dist2stack = 100
        self.destination = (100, 100)
        self.boxes_delivered = 0

    # ¿Qué pasará en cada unidad de tiempo?
    def step(self):
        #Si no tenemos una caja y la celda actual no es una caja, nos movemos de manera random
        if self.hasBox == False and self.order_box() == False:
            self.moveRandom()
        #Si recogemos una caja, no nos movemos 1 step
        elif self.order_box():
            pass
        #Si tenemos una caja, no podemos cargar más. Nos movemos a una pila
        elif self.hasBox:
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
        x, y = self.pos
        self.checkStackBoxState()
        available_stacks = []
        for agent in self.model.schedule.agents:
            if agent.unique_id >= 50 and agent.unique_id <= 53 and agent.isFull == False:
                available_stacks.append(agent.pos)
        
        #Calculamos las distancias del robot a las pilas
        for i in range(len(available_stacks)):
            dist = math.dist(self.pos, available_stacks[i])
            if dist < self.dist2stack:
                self.dist2stack = dist
                self.destination = available_stacks[i]
        
        #Tenemos 4 opciones de destino (4 pilas)
        #Cuadrante 1
        if self.destination == (11, 11):
            #Nos movemos según nuestra posición actual
            x_act, y_act = self.pos
            #Primero nos alineamos en el eje "x"
            if x_act < 11:
                new_position = (x + 1, y)
            elif x_act > 11:
                new_position = (x - 1, y)
            
            #Estamos alineados en "x", ahora nos movemos a y = 11
            elif y_act < 11:
                new_position = (x, y + 1)
            elif y_act > 11:
                new_position = (x, y - 1)

            #Ya estamos en la posición final
            else:
                self.hasBox = False
                self.boxes_delivered += 1
                self.model.unordered_boxes -= 1
                self.updateStackBox(11, 11)
                return
            
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

            return

        #Cuadrante 2
        elif self.destination == (1, 11):
            x_act, y_act = self.pos
            if x_act < 1:
                new_position = (x + 1, y)
            elif x_act > 1:
                new_position = (x - 1, y)
            elif y_act < 11:
                new_position = (x, y + 1)
            elif y_act > 11:
                new_position = (x, y - 1)
            else:
                self.hasBox = False
                self.boxes_delivered += 1
                self.model.unordered_boxes -= 1
                self.updateStackBox(1, 11)
                return
            
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            if len(cellmates) > 0:
                for c in cellmates:
                    if c.unique_id < 6:
                        self.model.grid.move_agent(self, self.pos)
                        return
            
            self.personal_steps += 1
            self.model.grid.move_agent(self, new_position)

            return

        #Cuadrante 3
        elif self.destination == (1, 1):
            x_act, y_act = self.pos
            if x_act < 1:
                new_position = (x + 1, y)
            elif x_act > 1:
                new_position = (x - 1, y)
            elif y_act < 1:
                new_position = (x, y + 1)
            elif y_act > 1:
                new_position = (x, y - 1)
            else:
                self.hasBox = False
                self.boxes_delivered += 1
                self.model.unordered_boxes -= 1
                self.updateStackBox(1, 1)
                return
            
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            if len(cellmates) > 0:
                for c in cellmates:
                    if c.unique_id < 6:
                        self.model.grid.move_agent(self, self.pos)
                        return
            
            self.personal_steps += 1
            self.model.grid.move_agent(self, new_position)

            return

        #Cuadrante 4
        elif self.destination == (11, 1):
            x_act, y_act = self.pos
            if x_act < 11:
                new_position = (x + 1, y)
            elif x_act > 11:
                new_position = (x - 1, y)
            elif y_act < 1:
                new_position = (x, y + 1)
            elif y_act > 1:
                new_position = (x, y - 1)
            else:
                self.hasBox = False
                self.boxes_delivered += 1
                self.model.unordered_boxes -= 1
                self.updateStackBox(11, 1)
                return
            
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            if len(cellmates) > 0:
                for c in cellmates:
                    if c.unique_id < 6:
                        self.model.grid.move_agent(self, self.pos)
                        return
            
            self.personal_steps += 1
            self.model.grid.move_agent(self, new_position)


            return


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
    
    def updateStackBox(self, x, y):
        for agent in self.model.schedule.agents:
            if agent.unique_id >= 50 and agent.unique_id <= 53 and agent.pos == (x, y):
                agent.box_counting += 1
                return
    
    def checkStackBoxState(self):
        for agent in self.model.schedule.agents:
            if agent.unique_id >= 50 and agent.unique_id <= 53 and agent.box_counting >= 5:
                agent.isFull = False
        

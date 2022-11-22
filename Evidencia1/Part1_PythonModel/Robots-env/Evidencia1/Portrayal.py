def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0
    }

    if agent.unique_id == 1:
        portrayal["Shape"] = "img/robots/Robot1.png"
        portrayal["r"] = 1
    elif agent.unique_id == 2:
        portrayal["Shape"] = "img/robots/Robot2.png"
        portrayal["r"] = 1
    elif agent.unique_id == 3:
        portrayal["Shape"] = "img/robots/Robot3.png"
        portrayal["r"] = 1
    elif agent.unique_id == 4:
        portrayal["Shape"] = "img/robots/Robot4.png"
        portrayal["r"] = 1
    elif agent.unique_id == 5:
        portrayal["Shape"] = "img/robots/Robot5.png"
        portrayal["r"] = 1

    elif agent.unique_id >= 50 and agent.unique_id < 90:
        # portrayal["Shape"] = "Shelf.png"
        if agent.box_counting == 0:
            portrayal["Shape"] = "img/numbers/five.png"
            portrayal["r"] = 0.2
        elif agent.box_counting == 1:
            portrayal["Shape"] = "img/numbers/four.png"
            portrayal["r"] = 0.2
        elif agent.box_counting == 2:
            portrayal["Shape"] = "img/numbers/three.png"
            portrayal["r"] = 0.2
        elif agent.box_counting == 3:
            portrayal["Shape"] = "img/numbers/two.png"
            portrayal["r"] = 0.2
        elif agent.box_counting == 4:
            portrayal["Shape"] = "img/numbers/one.png"
            portrayal["r"] = 0.2
        else:
            portrayal["Shape"] = "img/numbers/x.png"
            portrayal["r"] = 0.2
    elif agent.unique_id >= 100:
        # portrayal["Shape"] = "Shelf.png"
        # portrayal["Shape"] = "img/s2.jpg"
        portrayal["Shape"] = "img/warehouse.png"
        portrayal["r"] = 0.2
    else:
        portrayal["Shape"] = "img/box.png"
        portrayal["r"] = 0.2

    return portrayal
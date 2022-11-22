def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0
    }

    if agent.unique_id <= 5:
        portrayal["Shape"] = "img/Robot_pic.png"
        portrayal["r"] = 1,
    elif agent.unique_id >= 50 and agent.unique_id < 90:
        # portrayal["Shape"] = "Shelf.png"
        portrayal["Shape"] = "img/x.png"
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
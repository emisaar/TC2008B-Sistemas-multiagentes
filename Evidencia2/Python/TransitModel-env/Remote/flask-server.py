# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. November 2022

from flask import Flask, request, jsonify
# from boids.boid import Boid
from StreetModel import StreetModel
import json
import os

model = StreetModel()

# def updatePositions(flock):
#     positions = []
#     for boid in flock:
#         boid.apply_behaviour(flock)
#         boid.update()
#         boid.edges()
#         positions.append((boid.id, boid.position))
#     return positions

def positionsToJSON(positions):
    posDICT = []
    for p in positions:
        pos = {
            "vehicleId" : p[0],
            "x" : p[1],
            "y" : p[2],
            "z" : p[3]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

def lightsToJSON(lights):
    lightsDICT = []
    for l in lights:
        s = {
            "lightId" : l[0],
            "state" : l[1]
        }
        lightsDICT.append(s)
    return json.dumps(lightsDICT)

# Size of the board:
width = 21
height = 21

# Set the number of agents here:
# flock = []

app = Flask("Intersection Model", static_url_path='')
port=int(os.getenv('PORT',8000))

@app.route('/')
def root():
    return jsonify({'message':'Hello World!'})

@app.route('/init', methods=['POST', 'GET'])
def model_run():
    [positions, lights] = model.step()
    ans = "{ \"positions\": " + positionsToJSON(positions) + ",\"lights\": " + lightsToJSON(lights) + " }"
    return ans

if __name__=='__main__':
    app.run(host="0.0.0.0", port=port, debug=True)

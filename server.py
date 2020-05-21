from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Model

#function to define portrayal of filled cell
def mod_draw(agent):
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
    portrayal["Color"] = ["#FF0000", "#FF9999"]
    portrayal["stroke_color"] = "#00FF00"
    return portrayal

points = PointsElement()

#parameters of the arena and model
model_params = {
    "height": UserSettableParameter("slider", "Height", 50, 10, 50, 10),
    "width": UserSettableParameter("slider", "Width", 50, 10, 50, 10),
    "a_density": UserSettableParameter("slider", "Agent Density", 0.05, 0.05, 0.5, 0.05),
    "r_":UserSettableParameter("slider", "rate of reversals", 0, 0, 1, 0.25),
    "k_":UserSettableParameter("slider", "rate of switch", 0, 0, 1, 0.25),
}


canvas_element = CanvasGrid(mod_draw, 50, 50, 500, 500)

server = ModularServer(
    Model, [ canvas_element], "Model", model_params
)

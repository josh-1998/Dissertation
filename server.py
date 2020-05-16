from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Model

class PointsElement(TextElement):
    def __init__(self):
        pass
    def render(self,model):
        plist =[]
        str_build = ""

        return None#"Points of Optimum Oxygen Density: " + str(plist)

def mod_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
    portrayal["Color"] = ["#FF0000", "#FF9999"]
    portrayal["stroke_color"] = "#00FF00"
    return portrayal

points = PointsElement()

model_params = {
    "height": 50,
    "width": 50,
    "density": UserSettableParameter("slider", "Agent Density", 0.05, 0.05, 0.5, 0.05),
}


canvas_element = CanvasGrid(mod_draw, 50, 50, 500, 500)

server = ModularServer(
    Model, [ canvas_element], "Model", model_params
)

import pyglet
from OpenGL.GL import *
from math import cos, sin, pi
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica import basic_shapes as bs
from grafica import easy_shaders as es
from grafica import transformations as tr
from shapes_utils import HighLevelGPUShape, createGPUShape

class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Pyglet window"):
        super().__init__(width, height, title)
        self.total_time = 0
        self.fillPolygon = True
        self.pipeline = None
        self.repeats = 0

# We will use the global controller as communication with the callback function
WIDTH, HEIGHT = 1280, 800
controller = Controller(width=WIDTH, height=HEIGHT)
# Setting up the clear screen color
glClearColor(0.2, 0.7, 1, 0)

# Setting the model (data of our code)
# Creating our shader program and telling OpenGL to use it
pipeline = es.SimpleTransformShaderProgram()
controller.pipeline = pipeline
glUseProgram(pipeline.shaderProgram)

# Definimos las figuras
# Cuerpo de la mariposa
brown_body_vertices = [
    -0.01, -0.09, 0, 0.5, 0.1, 0,
    -0.01, 0.075, 0, 0.5, 0.1, 0, 
    0.01, 0.075, 0, 0.5, 0.1, 0,
    0.01, -0.09, 0, 0.5, 0.1, 0,
]
body_vertices = [
    0, 1, 2,
    0, 2, 3,
]
body = bs.Shape(brown_body_vertices, body_vertices)

# Alas de la mariposa
orange_wings_vertices = [
    -0.1, -0.065, 0, 1, 0.3, 0.1,
    -0.1, 0.065, 0, 1, 0.3, 0.1, 
    0.1, 0.065, 0, 1, 0.3, 0.1,
    0.1, -0.065, 0, 1, 0.3, 0.1,
]
wings_vertices = [
    0, 1, 2,
    0, 2, 3,
]
wings = bs.Shape(orange_wings_vertices, wings_vertices)

# Cuerpo de la mariposa verde
little_green_butterfly_body_vertices = [
    -0.01, -0.09, 0, 0, 0.2, 0,
    -0.01, 0.075, 0, 0, 0.2, 0, 
    0.01, 0.075, 0, 0, 0.2, 0,
    0.01, -0.09, 0, 0, 0.2, 0,
]
green_butterfly_body_vertices = [
    0, 1, 2,
    0, 2, 3,
]
little_green_body = bs.Shape(little_green_butterfly_body_vertices, green_butterfly_body_vertices)

# Alas de la mariposa verde
little_green_butterfly_wings_vertices = [
    -0.1, -0.065, 0, 0, 0.8, 0,
    -0.1, 0.065, 0, 0, 0.8, 0, 
    0.1, 0.065, 0, 0, 0.8, 0,
    0.1, -0.065, 0, 0, 0.8, 0,
]
green_butterfly_wings_vertices = [
    0, 1, 2,
    0, 2, 3,
]
little_green_wings = bs.Shape(little_green_butterfly_wings_vertices, green_butterfly_wings_vertices)

# Creamos los GPU
gpuBody = HighLevelGPUShape(pipeline, body)
gpuWings = HighLevelGPUShape(pipeline, wings)
gpulittlegreenBody = HighLevelGPUShape(pipeline, little_green_body)
gpulittlegreenWings = HighLevelGPUShape(pipeline, little_green_wings)

# Definimos las funciones que dibujan las partes de las mariposas
# Mariposa verde
def draw_green_wings(controller: Controller):
    gpulittlegreenWings.draw(controller.pipeline)
    gpulittlegreenWings.scale = tr.scale(0.8+0.4*sin(controller.total_time*2.5),1,0)
    gpulittlegreenWings.translation = tr.translate(0.5*sin(controller.total_time*2),0.5*sin(controller.total_time),0)

def draw_green_body(controller: Controller):
    gpulittlegreenBody.draw(controller.pipeline)
    gpulittlegreenBody.translation = tr.translate(0.5*sin(controller.total_time*2),0.5*sin(controller.total_time),0)

# Mariposa naranja
def draw_body(controller: Controller):
    gpuBody.draw(controller.pipeline)
    gpuBody.translation = tr.translate(0.3*cos(controller.total_time*3),0.15*sin(controller.total_time*3),0)

def draw_wings(controller: Controller):
    gpuWings.draw(controller.pipeline)
    gpuWings.scale = tr.scale(0.8+0.4*sin(controller.total_time*3),1,0)
    gpuWings.translation = tr.translate(0.3*cos(controller.total_time*3),0.15*sin(controller.total_time*3),0)

@controller.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        controller.close()

@controller.event
def on_draw():
    controller.clear()
    draw_wings(controller)
    draw_body(controller)
    draw_green_wings(controller)
    draw_green_body(controller)

def update(dt, controller):
   controller.total_time += dt

# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Set the view
pyglet.app.run()
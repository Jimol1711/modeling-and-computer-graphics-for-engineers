# coding=utf-8
"""Mariposa 3D"""

import os.path
import sys
import numpy as np
import pyglet
from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls

LIGHT_FLAT    = 0
LIGHT_GOURAUD = 1
LIGHT_PHONG   = 2

# Controlador que permite comunicarse con la ventana de pyglet
class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Mariposa 3D con ambiente"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        self.showAxis = True
        self.pipeline = None
        self.repeats = 0
        self.lightingModel = LIGHT_FLAT
        self.Texture = "wings_texture.jpg"
        # Dos variables que voy a usar para cambiar el punto de visión de la cámara. Voy variando las coordenadas del vector eye. 
        # Esto es la parte 3 del enunciado de la Tarea. 
        self.t = 1
        self.z = 0.8

# Se asigna el ancho y alto de la ventana y se crea.
WIDTH, HEIGHT = 1280, 600
controller = Controller(width=WIDTH, height=HEIGHT)
# Se asigna el color de fondo de la ventana
glClearColor(0.5843, 0.7568, 0.2274, 1)

# Como trabajamos en 3D, necesitamos chequear cuáles objetos están en frente, y cuáles detrás.
glEnable(GL_DEPTH_TEST)

# Se crean pipelines para cada programa de Shaders
textureFlatPipeline = ls.SimpleTextureFlatShaderProgram()
textureGouraudPipeline = ls.SimpleTextureGouraudShaderProgram()
texturePhongPipeline = ls.SimpleTexturePhongShaderProgram()

# Se crea otro pipeline sin texturas ni iluminación
colorPipeline = es.SimpleModelViewProjectionShaderProgram()

# Convenience function to ease initialization (En realidad solo la use para crear el GPU de los ejes)
def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

# GPU de los ejes
gpuAxis = createGPUShape(colorPipeline, bs.createAxis(4))

# Keys
@controller.event
def on_key_press(symbol, modifiers):
    # Toggle del fill pollygon
    if symbol == pyglet.window.key.SPACE:
        controller.fillPolygon = not controller.fillPolygon

    # Toggle entre ver los ejes y no (rojo = x, verde = y, azul = z)
    elif symbol == pyglet.window.key.LCTRL:
        controller.showAxis = not controller.showAxis

    # Cerrar la ventana
    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()

    # La cámara se va moviendo con las teclas RIGHT y LEFT. 
    # También se puede mover arriba y abajo con las teclas UP y DOWN.
    # Para volver a la posición inicial se presiona Z.
    elif symbol == pyglet.window.key.LEFT:
        controller.t += 0.1
    elif symbol == pyglet.window.key.RIGHT:
        controller.t += -0.1   
    elif symbol == pyglet.window.key.UP:
        controller.z += 0.1 
    elif symbol == pyglet.window.key.DOWN:
        controller.z += -0.1 
    elif symbol == pyglet.window.key.Z:
        controller.t = 1
        controller.z = 0.8
    # Toggle de los modos de iluminación
    elif symbol == pyglet.window.key.Q:
        controller.lightingModel = LIGHT_FLAT

    elif symbol == pyglet.window.key.W:
        controller.lightingModel = LIGHT_GOURAUD

    elif symbol == pyglet.window.key.E:
        controller.lightingModel = LIGHT_PHONG
    
    # Toggle de las texturas
    elif symbol == pyglet.window.key.D:
        controller.Texture = "wings_texture.jpg"

    elif symbol == pyglet.window.key.F:
        controller.Texture = "wings_texture2.jpg"
    else:
        print('Unknown key')

# Función para crear un cubo simple
def createCube():

    # Defining locations,texture coordinates and normals for each vertex of the shape  
    vertices = [
    #   positions            tex coords   normals
    # Z+
        -0.5, -0.5,  0.5,    0, 1,        0,0,1,
         0.5, -0.5,  0.5,    1, 1,        0,0,1,
         0.5,  0.5,  0.5,    1, 0,        0,0,1,
        -0.5,  0.5,  0.5,    0, 0,        0,0,1,   
    # Z-          
        -0.5, -0.5, -0.5,    0, 1,        0,0,-1,
         0.5, -0.5, -0.5,    1, 1,        0,0,-1,
         0.5,  0.5, -0.5,    1, 0,        0,0,-1,
        -0.5,  0.5, -0.5,    0, 0,        0,0,-1,
       
    # X+          
         0.5, -0.5, -0.5,    0, 1,        1,0,0,
         0.5,  0.5, -0.5,    1, 1,        1,0,0,
         0.5,  0.5,  0.5,    1, 0,        1,0,0,
         0.5, -0.5,  0.5,    0, 0,        1,0,0,   
    # X-          
        -0.5, -0.5, -0.5,    0, 1,        -1,0,0,
        -0.5,  0.5, -0.5,    1, 1,        -1,0,0,
        -0.5,  0.5,  0.5,    1, 0,        -1,0,0,
        -0.5, -0.5,  0.5,    0, 0,        -1,0,0,   
    # Y+          
        -0.5,  0.5, -0.5,    0, 1,        0,1,0,
         0.5,  0.5, -0.5,    1, 1,        0,1,0,
         0.5,  0.5,  0.5,    1, 0,        0,1,0,
        -0.5,  0.5,  0.5,    0, 0,        0,1,0,   
    # Y-          
        -0.5, -0.5, -0.5,    0, 1,        0,-1,0,
         0.5, -0.5, -0.5,    1, 1,        0,-1,0,
         0.5, -0.5,  0.5,    1, 0,        0,-1,0,
        -0.5, -0.5,  0.5,    0, 0,        0,-1,0
        ]   

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return bs.Shape(vertices, indices)

# Se crea la función que dibuja la mariposa, ahora con texturas. Para los otros objetos se hace lo mismo.
def createButterfly(pipeline,texture):

    # Creating shapes on GPU memory
    redCube = createCube()
    gpuredCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuredCube)
    gpuredCube.fillBuffers(redCube.vertices, redCube.indices, GL_STATIC_DRAW)
    gpuredCube.texture = es.textureSimpleSetup(
        "red_eyes_texture.jpg", GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    
    purpleCube = createCube()
    gpupurpleCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpupurpleCube)
    gpupurpleCube.fillBuffers(purpleCube.vertices, purpleCube.indices, GL_STATIC_DRAW)
    gpupurpleCube.texture = es.textureSimpleSetup(
        "purple_body_texture.jpg", GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    whiteCube = createCube()
    gpuwhiteCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuwhiteCube)
    gpuwhiteCube.fillBuffers(whiteCube.vertices, whiteCube.indices, GL_STATIC_DRAW)
    gpuwhiteCube.texture = es.textureSimpleSetup(
        texture, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    cianCube = createCube()
    gpucianCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpucianCube)
    gpucianCube.fillBuffers(cianCube.vertices, cianCube.indices, GL_STATIC_DRAW)
    gpucianCube.texture = es.textureSimpleSetup(
        "cian_texture.jpg", GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    # Creating the body of the butterfly
    body = sg.SceneGraphNode("body")
    body.transform = tr.matmul([tr.scale(0.04,0.07,0.22), tr.translate(0,0,0.975)])
    body.childs += [gpupurpleCube]

    # Creating the wings of the butterfly
    wing1 = sg.SceneGraphNode("wing1")
    wing1.childs += [gpuwhiteCube]

    wing2 = sg.SceneGraphNode("wing2")
    wing2.childs += [gpuwhiteCube]

    wing3 = sg.SceneGraphNode("wing3")
    wing3.childs += [gpuwhiteCube]

    wing4 = sg.SceneGraphNode("wing4")
    wing4.childs += [gpuwhiteCube]

    # Creating the eyes and nose of the butterfly
    eye1 = sg.SceneGraphNode("eye1")
    eye1.transform = tr.matmul([tr.scale(0.02,0.02,0.02), tr.translate(-1.2,1,14.5)])
    eye1.childs += [gpuredCube]

    eye2 = sg.SceneGraphNode("eye2")
    eye2.transform = tr.matmul([tr.scale(0.02,0.02,0.02), tr.translate(-1.2,-1,14.5)])
    eye2.childs += [gpuredCube]

    nose = sg.SceneGraphNode("nose")
    nose.transform = tr.matmul([tr.scale(0.02,0.02,0.01), tr.translate(-1.2,0,27)])
    nose.childs += [gpucianCube]

    # Creating the butterfly hierarchy
    butterfly = sg.SceneGraphNode("butterfly")
    butterfly.childs += [body]
    butterfly.childs += [wing1]
    butterfly.childs += [wing2]
    butterfly.childs += [wing3]
    butterfly.childs += [wing4]
    butterfly.childs += [eye1]
    butterfly.childs += [eye2]
    butterfly.childs += [nose]

    return butterfly

# Se crea la función que dibuja los árboles
def createTree(pipeline):

    # Creating shapes on GPU memory
    brownCube = createCube()
    gpubrownCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpubrownCube)
    gpubrownCube.fillBuffers(brownCube.vertices, brownCube.indices, GL_STATIC_DRAW)
    gpubrownCube.texture = es.textureSimpleSetup(
        "wood_tree_texture.jpg", GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    greenCube = createCube()
    gpugreenCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpugreenCube)
    gpugreenCube.fillBuffers(greenCube.vertices, greenCube.indices, GL_STATIC_DRAW)
    gpugreenCube.texture = es.textureSimpleSetup(
        "leaves.jpg", GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    # Creating the trunk of the tree
    trunk = sg.SceneGraphNode("trunk")
    trunk.transform = tr.matmul([tr.scale(0.04,0.04,0.22), tr.translate(0,0,0.975)])
    trunk.childs += [gpubrownCube]

    # Creating the leaves of the trees
    upperLeaves = sg.SceneGraphNode("upperLeaves")
    upperLeaves.transform = tr.matmul([tr.scale(0.1,0.1,0.05), tr.translate(0,0,5.9)])
    upperLeaves.childs += [gpugreenCube]

    lowerLeaves = sg.SceneGraphNode("lowerLeaves")
    lowerLeaves.transform = tr.matmul([tr.scale(0.05,0.05,0.05), tr.translate(0,0,6.4)])
    lowerLeaves.childs += [gpugreenCube]

    # Creating the tree hierarchy
    tree = sg.SceneGraphNode("tree")
    tree.childs += [trunk]
    tree.childs += [upperLeaves]
    tree.childs += [lowerLeaves]

    return tree

# Función que crea un conejo para el extra
def createBunny(pipeline):

    # Creating shapes on GPU memory
    whiteCube = createCube()
    gpuwhiteCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuwhiteCube)
    gpuwhiteCube.fillBuffers(whiteCube.vertices, whiteCube.indices, GL_STATIC_DRAW)
    gpuwhiteCube.texture = es.textureSimpleSetup(
        "bunny_fur_texture.jpg", GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    # Creating the body of the bunny
    body = sg.SceneGraphNode("body")
    body.transform = tr.matmul([tr.scale(0.09,0.05,0.07), tr.translate(0,0,0.975)])
    body.childs += [gpuwhiteCube]

    head = sg.SceneGraphNode("head")
    head.transform = tr.matmul([tr.scale(0.05,0.05,0.05), tr.translate(0.9,0,2)])
    head.childs += [gpuwhiteCube]

    # Creating the ears and eyes of the bunny
    rightEar = sg.SceneGraphNode("rightEar")
    rightEar.transform = tr.matmul([tr.rotationZ(0.45),tr.scale(0.007,0.02,0.05), tr.translate(3.5,-1.3,3)])
    rightEar.childs += [gpuwhiteCube]

    leftEar = sg.SceneGraphNode("leftEar")
    leftEar.transform = tr.matmul([tr.rotationZ(-0.45),tr.scale(0.007,0.02,0.05), tr.translate(3.5,1.3,3)])
    leftEar.childs += [gpuwhiteCube]

    # Creating the bunny hierarchy
    bunny = sg.SceneGraphNode("bunny")
    bunny.childs += [body]
    bunny.childs += [head]
    bunny.childs += [rightEar]
    bunny.childs += [leftEar]

    return bunny

# Se crea todo lo necesario para el modelo 3D
# En este caso se usa un modelo en format OFF
# Esto corresponde a la parte 5 de la tarea 2, parte 1 de la tarea 3
# Función que crea la gpuShape del modelo 3D
def createOFFShape(pipeline, filename, r,g, b):
    shape = readOFF(filename, (r, g, b))
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

# Función que lee los vértices del modelo 3D
def readOFF(filename, color):
    vertices = []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        print(f'Vertices shape: {vertices.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)

        print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexDataF, indices)

# Se crea la GPUShape del dragon
dragon = createOFFShape(colorPipeline,'dragon.off',0.9,0.9,0.7)

# Aquí se crean las figuras en la memoria de la GPU. La de la mariposa incluye la textura del controlador para poder cambiarla con input del usuario.
butterflyNode = createButterfly(textureGouraudPipeline,controller.Texture)
treeNode = createTree(textureGouraudPipeline)
bunnyNode = createBunny(textureGouraudPipeline)

# Esta función se ejecuta aproximadamente 60 veces por segundo, dt es el tiempo entre la última
# ejecución y ahora
def update(dt, window):
    window.total_time += dt

# Cada vez que se llama update(), se llama esta función también
@controller.event
def on_draw():
    controller.clear()

    # Si el controller está en modo fillPolygon, dibuja polígonos. Si no, líneas.
    if controller.fillPolygon:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    # Lo siguiente es definir la vista de la cámara
    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(WIDTH)/float(HEIGHT), 0.1, 100)

    view = tr.lookAt(
            np.array([np.sqrt(2)*np.sin(controller.t),np.sqrt(2)*np.cos(controller.t),controller.z]),
            np.array([0,0,0]),
            np.array([0,0,1])
        )

    if controller.showAxis:
        glUseProgram(colorPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(colorPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        colorPipeline.drawCall(gpuAxis, GL_LINES)
    
    # Selecting the lighting shader program
    if controller.lightingModel == LIGHT_FLAT:
            lightingPipeline = textureFlatPipeline
    elif controller.lightingModel == LIGHT_GOURAUD:
            lightingPipeline = textureGouraudPipeline
    elif controller.lightingModel == LIGHT_PHONG:
            lightingPipeline = texturePhongPipeline
    else:
        raise Exception()

    glUseProgram(lightingPipeline.shaderProgram)

    # Setting all uniform shader variables
        
    # White light in all components: ambient, diffuse and specular.
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    # Object is barely visible at only ambient. Bright white for diffuse and specular components.
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    # TO DO: Explore different parameter combinations to understand their effect!
    
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -5, -5, 5)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), np.sqrt(2)*np.sin(controller.t), np.sqrt(2)*np.cos(controller.t), controller.z)
    glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)

    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    butterflyNode = createButterfly(textureGouraudPipeline,controller.Texture)
    # Acá se define el movimiento continuo como las alas y de toda la mariposa
    # Corresponde a la parte 1 del enunciado (movimiento de las alas) y a la parte 2 (movimiento de la mariposa)
    wing1 = sg.findNode(butterflyNode, "wing1")
    wing2 = sg.findNode(butterflyNode, "wing2")
    wing3 = sg.findNode(butterflyNode, "wing3")
    wing4 = sg.findNode(butterflyNode, "wing4")
    wing1.transform = tr.matmul([tr.rotationZ(0.45*np.cos(np.pi*controller.total_time)+1.1), tr.scale(0.2,0.002,0.12), tr.translate(0.5,-1,2)])
    wing2.transform = tr.matmul([tr.rotationZ(-0.45*np.cos(np.pi*controller.total_time)-1.1), tr.scale(0.2,0.002,0.12), tr.translate(0.5,1,2)])
    wing3.transform = tr.matmul([tr.rotationZ(0.45*np.cos(np.pi*controller.total_time)+1.1), tr.scale(0.13,0.002,0.06), tr.translate(0.5,-1,2.5)])
    wing4.transform = tr.matmul([tr.rotationZ(-0.45*np.cos(np.pi*controller.total_time)-1.1), tr.scale(0.13,0.002,0.06), tr.translate(0.5,1,2.5)])
    butterflyNode.transform = tr.matmul([tr.rotationZ(np.pi/4*controller.total_time),tr.translate(0.4*np.sin(controller.total_time*0.5)+0.2,0.4*np.cos(controller.total_time*0.5)+0.2,0.3*np.sin(controller.total_time*0.8)+0.5)])

    #Acá se dibujan todas las figuras del grafo de escena
    # Dibujamos la mariposa
    sg.drawSceneGraphNode(butterflyNode, lightingPipeline, "model", tr.uniformScale(0.4))
    
    # Dibujamos MUCHOS árboles para crear un bosque (parte 4 de la tarea 2, 1 de la tarea 3)
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model",tr.translate(0.8,0.8,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.3,0.2,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.1,0.9,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.6,-0.4,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.9,-0.1,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.7, 0.3,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.2, -0.9,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.1, 0.8,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.5, -0.4,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.9, -0.2,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.6, 0.7,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.1, -0.5,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.4, 0.6,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.8, -0.8,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.3, -0.1,0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.9, 0.1, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.3, 0.5, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.6, -0.2, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.7, -0.4, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.3, 0.9, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.1, -0.8, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.4, 0.2, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.8, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.7, -0.3, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.5, 0.1, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.2, -0.5, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.7, 0.9, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.1, 0.7, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.6, -0.8, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.8, 0.3, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.3, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.2, 0.4, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.8, -0.1, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.5, -0.2, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.6, 0.2, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.8, 0.2, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.3, -0.7, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.6, 0.8, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.5, -0.2, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.1, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.7, -0.3, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.2, 0.4, 0)) 
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.4, 0.7, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.2, -0.3, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.9, 0.5, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.7, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.4, 0.9, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(-0.3, -0.8, 0))
    sg.drawSceneGraphNode(treeNode, lightingPipeline, "model", tr.translate(0.8, -0.4, 0))

    # Dibujamos el conejo (Extra de la tarea 2)
    sg.drawSceneGraphNode(bunnyNode, lightingPipeline, "model", tr.translate(0,0.5,0.1*np.cos(5*controller.total_time)+0.07))

    # Para todo lo dibujado anteriormente se utiliza lightingPipeline, que corresponde al pipeline de las texturas y de la iluminación.

    # Se dibuja el dragon (parte 5 de la tarea 2 y 1 de la tarea 3) se cambia de pipeline.
    glUseProgram(colorPipeline.shaderProgram)
    colorPipeline.drawCall(dragon, GL_TRIANGLES)

# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Se ejecuta la aplicación
pyglet.app.run()
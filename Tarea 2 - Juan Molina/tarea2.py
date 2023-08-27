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

# Controlador que permite comunicarse con la ventana de pyglet
class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Mariposa 3D con ambiente"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        self.showAxis = True
        self.pipeline = None
        self.repeats = 0

# Se asigna el ancho y alto de la ventana y se crea.
WIDTH, HEIGHT = 1280, 600
controller = Controller(width=WIDTH, height=HEIGHT)
# Se asigna el color de fondo de la ventana
glClearColor(0.5843, 0.7568, 0.2274, 1)

# Como trabajamos en 3D, necesitamos chequear cuáles objetos están en frente, y cuáles detrás.
glEnable(GL_DEPTH_TEST)

# Se configura el pipeline y se le dice a OpenGL que utilice ese shader
mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
controller.pipeline = mvpPipeline
glUseProgram(mvpPipeline.shaderProgram)

# Dos variables que voy a usar para cambiar el punto de visión de la cámara. Voy variando las coordenadas del vector eye. 
# Esto es la parte 3 del enunciado de la Tarea. 
t = 1
z = 0.8

# Keys
@controller.event
def on_key_press(symbol, modifiers):
    global t, z
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
        t += 0.1
    elif symbol == pyglet.window.key.RIGHT:
        t += -0.1   
    elif symbol == pyglet.window.key.UP:
        z += 0.1 
    elif symbol == pyglet.window.key.DOWN:
        z += -0.1 
    elif symbol == pyglet.window.key.Z:
        t = 1
        z = 0.8
    else:
        print('Unknown key')

# Se crea la función que dibuja la mariposa
def createButterfly(pipeline):

    # Creating shapes on GPU memory
    redCube = bs.createColorCube(0.658,0.168,0.262)
    gpuredCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuredCube)
    gpuredCube.fillBuffers(redCube.vertices, redCube.indices, GL_STATIC_DRAW)

    purpleCube = bs.createColorCube(0.6,0.55,0.76)
    gpupurpleCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpupurpleCube)
    gpupurpleCube.fillBuffers(purpleCube.vertices, purpleCube.indices, GL_STATIC_DRAW)

    whiteCube = bs.createColorCube(0.86,0.94,0.92)
    gpuwhiteCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuwhiteCube)
    gpuwhiteCube.fillBuffers(whiteCube.vertices, whiteCube.indices, GL_STATIC_DRAW)

    cianCube = bs.createColorCube(0.494,0.73,0.768)
    gpucianCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpucianCube)
    gpucianCube.fillBuffers(cianCube.vertices, cianCube.indices, GL_STATIC_DRAW)

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
    brownCube = bs.createColorCube(0.7,0.3,0.1)
    gpubrownCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpubrownCube)
    gpubrownCube.fillBuffers(brownCube.vertices, brownCube.indices, GL_STATIC_DRAW)

    greenCube = bs.createColorCube(0,0.6,0.1)
    gpugreenCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpugreenCube)
    gpugreenCube.fillBuffers(greenCube.vertices, greenCube.indices, GL_STATIC_DRAW)

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
    whiteCube = bs.createColorCube(0.9,0.9,0.6)
    gpuwhiteCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuwhiteCube)
    gpuwhiteCube.fillBuffers(whiteCube.vertices, whiteCube.indices, GL_STATIC_DRAW)

    blackCube = bs.createColorCube(0,0,0)
    gpublackCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpublackCube)
    gpublackCube.fillBuffers(blackCube.vertices, blackCube.indices, GL_STATIC_DRAW)

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

    Eye1 = sg.SceneGraphNode("Eye1")
    Eye1.transform = tr.matmul([tr.scale(0.01,0.01,0.01), tr.translate(7,-1.3,11)])
    Eye1.childs += [gpublackCube]

    Eye2 = sg.SceneGraphNode("Eye2")
    Eye2.transform = tr.matmul([tr.scale(0.01,0.01,0.01), tr.translate(7,1.3,11)])
    Eye2.childs += [gpublackCube]

    # Creating the bunny hierarchy
    bunny = sg.SceneGraphNode("bunny")
    bunny.childs += [body]
    bunny.childs += [head]
    bunny.childs += [rightEar]
    bunny.childs += [leftEar]
    bunny.childs += [Eye1]
    bunny.childs += [Eye2]

    return bunny

# Se crea todo lo necesario para el modelo 3D
# En este caso se usa un modelo en format OFF
# Esto corresponde a la parte 5 de la tarea
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
dragon = createOFFShape(mvpPipeline,'dragon.off',0.9,0.9,0.7)

# Creating shapes on GPU memory
cpuAxis = bs.createAxis(7)
gpuAxis = es.GPUShape().initBuffers()
mvpPipeline.setupVAO(gpuAxis)
gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

# Aquí se crean las figuras en la memoria de la GPU
butterflyNode = createButterfly(mvpPipeline)
treeNode = createTree(mvpPipeline)
bunnyNode = createBunny(mvpPipeline)

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
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE,
                       projection)

    view = tr.lookAt(
            np.array([np.sqrt(2)*np.sin(t),np.sqrt(2)*np.cos(t),z]),
            np.array([0,0,0]),
            np.array([0,0,1])
        )
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    if controller.showAxis:
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE,
                           tr.identity())
        mvpPipeline.drawCall(gpuAxis, GL_LINES)
    
    # Se dibuja el dragon (parte 5 de la tarea)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE,
                           tr.identity())
    mvpPipeline.drawCall(dragon, GL_TRIANGLES)
    
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
    sg.drawSceneGraphNode(butterflyNode, mvpPipeline, "model", tr.uniformScale(0.4))
    
    # Dibujamos MUCHOS árboles para crear un bosque (parte 4 de la tarea)
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model",tr.translate(0.8,0.8,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.3,0.2,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.1,0.9,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.6,-0.4,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.9,-0.1,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.7, 0.3,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.2, -0.9,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.1, 0.8,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.5, -0.4,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.9, -0.2,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.6, 0.7,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.1, -0.5,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.4, 0.6,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.8, -0.8,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.3, -0.1,0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.9, 0.1, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.3, 0.5, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.6, -0.2, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.7, -0.4, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.3, 0.9, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.1, -0.8, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.4, 0.2, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.8, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.7, -0.3, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.5, 0.1, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.2, -0.5, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.7, 0.9, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.1, 0.7, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.6, -0.8, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.8, 0.3, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.3, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.2, 0.4, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.8, -0.1, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.5, -0.2, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.6, 0.2, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.8, 0.2, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.3, -0.7, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.6, 0.8, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.5, -0.2, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.1, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.7, -0.3, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.2, 0.4, 0)) 
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.4, 0.7, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.2, -0.3, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.9, 0.5, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.7, -0.6, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.4, 0.9, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(-0.3, -0.8, 0))
    sg.drawSceneGraphNode(treeNode, mvpPipeline, "model", tr.translate(0.8, -0.4, 0))

    # Dibujamos el conejo (Extra de la tarea)
    sg.drawSceneGraphNode(bunnyNode, mvpPipeline, "model", tr.translate(0,0.5,0.1*np.cos(5*controller.total_time)+0.07))

# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Se ejecuta la aplicación
pyglet.app.run()
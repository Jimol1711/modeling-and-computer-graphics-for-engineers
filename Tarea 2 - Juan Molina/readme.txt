Nombre: Juan Ignacio Molina

Para la tarea se utilizaron los módulos de la carpeta grafica y los módulos Pyglet y OpenGL. Lo necesario para que se ejecute el programa esta todo en la tarea.  

En la carpeta entregada se encuentran la carpeta grafica, la tarea, un modelo 3D de la cabeza de un dragon en formato OFF y un ejemplo 
que encontré en la carpeta examples del repositorio de donde saqué dos funciones (Además de este archivo readme).

Partes 1 y 2 de la tarea
La tarea grafica una mariposa simple creada con polígonos (Cubos) la cual mueve las alas y se mueve en la escena. Se crea una función createButterfly en la cual se definen
las partes de la mariposa como el cuerpo y las alas y se dibujan utilizando grafo de escena. En la función on_draw se define el movimiento de las alas y de la mariposa.
Después se define el nodo de la mariposa y se dibuja la mariposa con drawSceneGraphNode.

Parte 3 de la tarea
Para el movimiento de la camara definí dos variables t y z. t es una variable que aumenta con el input del usuario, específicamente al presionar las teclas RIGHT y LEFT. 
Esta variable esta dentro de los parámetros x e y del primer arreglo la función lookAt, ya que dicho arreglo corresponde al vector Eye, el cual define el punto desde el cual 
ve la cámara. Los parámetros x e y van variando con t en la forma de una circunferencia parametrizada, con lo que al presionar RIGHT o LEFT la cámara se mueve en una
trayectoria circunferencial alrededor de la escena según la tecla correspondiente (RIGHT hacia la derecha, LEFT hacia la izquierda). La variable z sirve para aumentar o
disminuir la altura desde la cual ve la cámara, con lo que al presionar UP o DOWN la cámara verá desde más arriba o más abajo correspondientemente. Todo esto permite
un movimiento libre alrededor de la escena y poder ver todos sus elementos desde cualquier punto del espacio 3D. Cabe destacar que la cámara siempre mantiene a la mariposa 
dentro de su angulo de visión.

Parte 4 de la tarea
Luego se creo una función que dibuja un árbol hecho con cubos. Esta función se llama muchas veces dentro de on_draw pero en posiciones distintas cada vez. Esto se hace con el
objetivo de crear un bosque y cumplir con la parte 4 de la tarea.

Parte 5 de la tarea
Se obtuvo un archivo en formato OFF de internet, pero lamentablemente perdí el link de la página de internet donde lo conseguí. El formato OFF es una formato bastante sencillo
el cual contiene los vertices de la figura en sus primera líneas y después todas las lineas que empiezan por 3 contienen los índices que indican como se unen los vértices.
La primera línea siempre dice "OFF". De leer el archivo OFF se encarga la función readOFF dentro de la tarea. Esta función la saqué de un ejemplo del repositorio llamado
"ex_curve_demo.py" en la carpeta "examples", pero la modifiqué para que no considerara texturas ni normales. La función readOFF se asegura que sea un archivo OFF viendo que la primera linea diga
"OFF" y después extrae los vertices y los índices. Después se usa la función createOFFShape (también sacada del ejemplo mencionado antes) para crear la gpuShape de la figura que se busca 
modelar. Luego se define la variable dragon, que corresponde a la gpuShape creada con la función anterior de un archivo OFF el cual contiene los vertices e índices de la
figura de la cabeza de un dragon. Finalmente dentro de on_draw se llama a la función drawCall de OpenGL con el pipeline de la ventana de Pyglet, con la gpuShape definida como dragon y
con el argumento GL_TRIANGLES para que la figura dibujada contenga triangulos llenos y no solamente líneas.

Parte extra de la tarea
Como extra se creo un conejo saltarín que acompaña a la mariposa en la escena. Se creo de la misma forma que la mariposa, con una función y con jerarquía de nodos y grafo de 
escena, y se definió el movimiento del salto dentro de on_draw.

Con todo esto, la tarea muestra una escena de un bosque con el cráneo de un dragon milenario, el cual tiene a una mariposa que vuela por la escena, incluso pasando por
entremedio de la boca del dragon, y un conejo que salta.

Cabe destacar que se mantuvieron algunas funciones del auxiliar 4 como el usar la tecla Ctrl para togglear entre que se vean o no los ejes. Por lo tanto para ver bien la escena 
sin los ejes simplemente se debe presionar Ctrl. Esto lo dejé porque me ayudo para poder graficar las figuras. También se mantuvo que la tecla SPACE rellene los polígonos y que con
ESC se cierre la ventana de Pyglet.





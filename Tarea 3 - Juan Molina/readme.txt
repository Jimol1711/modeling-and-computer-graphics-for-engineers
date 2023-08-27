Nombre: Juan Ignacio Molina

Para la tarea se utilizaron los módulos de la carpeta grafica y los módulos Pyglet y OpenGL. Lo necesario para que se ejecute el programa esta todo en la tarea.

En la carpeta entregada se encuentran la carpeta grafica, la tarea, un modelo 3D de la cabeza de un dragon en formato OFF, muchos archivos JPG que corresponden a todas las texturas
aplicadas a objetos de la tarea.

Parte 1 de la Tarea
Esto corresponde a todos los requisitos de la Tarea 2. Todo esto se cumple (Mariposa que vuela en escenario 3D que se puede ver moviendo la cámara con modelo 3D sacado de internet
y un extra que corresponde a un conejo que salta).

Parte 2
Esto corresponde a la iluminación. Se definen 3 pipelines de iluminación para las distintas técnicas (Iluminación local plana, Gouraud y Phong). Se asignan todas las variables de 
iluminación dentro de la función on_draw. Se puede cambiar entre las distintas técnicas de iluminación con las teclas Q, W y E. Notar que no solo se ilumina la mariposa si no que 
también todo el escenario y el conejo. Lo único que no se ilumina es el dragon.

Parte 3
La parte 3 son las texturas. Se le aplicaron texturas a la mariposa, no solo a las alas, sin que además se le aplicaron texturas a todos los objetos que la componen. Esto se hizo 
modificando la funcion que crea la mariposa, creando cubos con texturas y además se utiliza otro pipeline el cual es el mismo que el de iluminación. Además, la textura se puede
cambiar con las teclas D y F, que también es uno de los requisitos de la parte 3. Las texturas utilizadas están en la carpeta en formato JPG.

Parte Extra
Para la parte extra estan las texturas aplicadas a los demás objetos de la escena, los arboles y el conejo. Todas las texturas de estos objetos están en el Zip. Además se aplicó
iluminación a estos objetos (Lo cual no está especificado en la tarea.)

En la tarea anterior puse que había perdido la página web de donde saqué el modelo 3D, pero la encontré! Corresponde al siguiente link: http://www.holmes3d.net/graphics/offfiles/

Con todo esto, la tarea muestra una escena de un bosque con el cráneo de un dragon milenario, el cual tiene a una mariposa que vuela por la escena con texturas e iluminación, 
incluso pasando por entremedio de la boca del dragon, y un conejo que salta y árboles que componen un bosque también con texturas e iluminación.
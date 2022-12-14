# 馃 Duckiebot interactivo
Este proyecto, desarrollado por [Nacho Dagach](https://github.com/ignaciodagachabugattas), [Pichi](https://github.com/pichiuwu) y [Max](https://github.com/maxfloresv), se est谩 realizando para el curso **CD2201 M贸dulo Interdisciplinario** (Duckietown).

Recomendamos leas esta guia tras haber visto el video de demostraci贸n del proyecto en el siguiente [link](https://www.youtube.com/watch?v=ZXwcHaN6O-M&ab_channel=ProfeNacho), para que lo conozcas de primera mano, pata o ala, seg煤n corresponda.

Se trata de un robot que escucha instrucciones y responde mediante voz. Algunas de las interacciones adicionales que se buscan implementar son:

* Gama completa de movimientos comandados por voz.
* Hacer que el Duckiebot pueda decir datos curiosos/chistes.
* Hacer que el Duckiebot sea capaz de cantar y bailar con una instrucci贸n.
* Agregar palabras clave ocultas de interacci贸n para realizar acciones secretas (*Easter Eggs*).

La informaci贸n sobre los avances del proyecto puede ser encontrada en la [wiki](https://github.com/maxfloresv/robot_interactivo/wiki).

### 馃幃 Manejo del Joystick
Para el desarrollo del proyecto, se ocup贸 un control de Xbox 360, y se usaron los siguientes botones:
* Palanca izq. para el giro (3 en la imagen).
* LT para retroceder (6 en la imagen). 
* RT para acelerar (9 en la imagen).

La referencia al control est谩 en la funci贸n `callback_control` del [archivo principal](https://github.com/maxfloresv/robot_interactivo/blob/main/duckiebot.py).

![d10437ca-81da-48db-a7a0-4c1173ad42e1](https://user-images.githubusercontent.com/45862114/199054372-978e232f-ea52-479f-8155-ffc665857241.png)

### 馃摎 Comandos y definiciones 煤tiles:
El siguiente enlace [(click ac谩)](https://colab.research.google.com/drive/12NgKqmJJR6yABCUIHCZr6NJvG4wegARU) contiene una gu铆a sobre el uso del Duckiebot.

### 馃懢驴C贸mo lo utilizamos?
**Necesitar谩s conexi贸n estable a internet!!**

Para comenzar a utilizar el Duckiebot, se debe seguir lo siguiente. 

Primero se abre la consola en la cual se debe ingresar al Duckiebot utilizando `ssh -X duckiebot@duckiebot.local` y se ingresa la contrase帽a. Luego se abren las carpetas ingresando `cd \duckiebot\catkin_ws\src\desafios_2022\src`. Se ejecuta `roslaunch ros_cap duckie_core.local` y se ejecuta el programa en una nueva terminal desde el duckiebot con `rosrun desafios_2022 duckiebot.py`.

Para esto se abre una nueva terminal y se utiliza `ifconfig` la cual se usa para configurar y ver el estado de las interfaces de red en los sistemas operativos Linux. 

Luego copiamos la IP encontrada y conectamos el duckiebot con el computador a trav茅s de `export ROS_IP=...` y pegamos justo a continuaci贸n la IP copiada anteriormente. 
Se ejecuta `cd duckiebot_pc` y luego `python3 voice2text.py` para ejecutar el programa desde el PC.

Para que el Duckiebot comience a recibir instrucciones por voz se presiona el bot贸n A en el Joystick. Cuando responde "quack quack" se le entrega la instrucci贸n y se ver谩 en la consola la instrucci贸n recibida.

### 馃搫 Documentaci贸n adicional:
Por un lado, en el archivo **duckiebot.py**:

+ Encontramos la librer铆a `pyttsx3` hace hablar al programa por los altavoces, es decir Text-to-Speech. Luego se establecen las propiedades de esta voz como el idioma y el volumen al cual sale por el parlante.

+ Luego, se define la funci贸n tiempo la cual al ingresar un 谩ngulo, calcula el tiempo que le toma al Duckiebot girar en ese 谩ngulo. Para esto calculamos con cron贸metro que el Duckiebot se demora 1.5 segundos.

  Luego, definimos las propiedades del inicializador en el cual est谩n los Subscribers los cuales reciben informaci贸n del Joystick, del tiempo en que queremos que gire, de la voz y de wikipedia.
Adem谩s definimos los Publishers los cuales publican la informaci贸n recibida a las ruedas y al parlante. Las siguientes son propiedades del estado inicial del Duckiebot y propiedades que se le asignan a cada instrucci贸n para el momento de ejecutarlas.
Estas 煤ltimas est谩n dadas por \[rapidez lineal, rapidez angular, tiempo de ejecuci贸n].

+ Se define la funci贸n `callback_control(self, msg)` la cual le asigna a cada bot贸n de joystick y movimiento de las ruedas cambiando su velocidad lineal o angular. Tambi茅n se define el bot贸n B como freno de emergencia y el freno si se presiona acelerar y retroceder al mismo tiempo.

+ Se utiliza la **distancia de Levenshtein** la cual nos entrega el n煤mero m铆nimo de operaciones que se deben hacer para transformar un string en otro. 脡stas operaciones son agregar, eliminar o sustituir un elemento de este string. Definimos esta funci贸n para que si decimos \"avanzar" y el duckiebot detecta \"avanza", realice igual la acci贸n. 

+ Se define `ejecutar_instrucci贸n` la cual ejecuta una instrucci贸n que se haya pedido, devolviendo False si no coincide con las funciones que se agregan y True si es la indicada y se ejecut贸 la acci贸n. 脡sto se realiza s贸lo si la palabra que se obtuvo tiene menos de 2 operaciones de diferencia con las indicadas (distancia de Levenshtein < 2) y para las instrucciones avanzar y retroceder pregunta de vuelta el tiempo en que se quiere que se realice la acci贸n y se publica el tiempo ingresado. `sleep` es una funci贸n que permite detener un programa durante un tiempo y luego permitir que contin煤e sin alteraciones, en nuestro caso durante 5 segundos (para esperar el *input* por voz).

+ En la funci贸n `callback_voz` se extraen las propiedades de las acciones recibidas antteriormente y si se ejecuta la acci贸n se detiene el Duckiebot. Adem谩s, se definen las propiedades de la funci贸n bailar, las cuales son tocar una canci贸n random entre las definidas, avanzar y retroceder (instrucci贸n de la 1 a la 5) y girar a la izquierda y a la derecha (instrucci贸n de la 6 a la 9). Luego se publica este mensaje en las ruedas para ejecutar la acci贸n. Luego de pasar el tiempo, se detiene el Duckiebot. 
  
+ La funci贸n `callback_tiempo` transforma a entero el tiempo ingresado y cambia a True la variable `valid` si se ingresa un numero entero positivo o cero.
+ La funci贸n `callback_wiki` recibe los datos obtenidos de Wikipedia y los imprime en la consola.

Por otro lado, en el archivo **voice2text**:
+ Luego de importar las librer铆as se establece el lenguaje espa帽ol de la Wikipedia. Y se define `run = True` el cual define si corre o no el programa.

+ Se define el objeto de la clase en el cual se definen sus propiedades como los Publishers de voz a texto, de tiempo y de la b煤squeda en Wikipedia, adem谩s de los Subscribers del Joystick y de la publicaci贸n de mensaje de Wikipedia. 
  El programa de voz est谩 dado por `sr.Recognizer()` y se define las propiedades A y X como 0.
  
+ Se define el `callback` en la cual se encuentran las valiables globales run y active. Se utiliza el bot贸n X como un t茅rmino de emergencia del programa ya que deja de correr este 煤ltimo. Luego, se utiliza el bot贸n A para ejecutar el micr贸fono. En el caso en que sea una llamada forzada de la funci贸n, la variable `auto = True` por lo que, por ejemplo si se recibe la instrucci贸n avanzar, devolver谩 "Quack avanzar".

+ Dentro del bloque `try`, se intenta capturar las instrucciones de voz. Si ocurre alg煤n error, pasa al bloque `except` donde el error en cuesti贸n es imprimido en la consola (para *debuggear*).

+ Luego, `callback_control` a partir de la lista que recupera la posici贸n de cada bot贸n del Joystick, se le asigna la variable A al bot贸n "A" del joystick y lo mismo con el bot贸n "X".

+ La funci贸n `callback_req` recibe una instrucci贸n del Duckiebot ("tiempo" o "buscar"), lo que hace que se llame a la funci贸n que pide *inputs* de voz. Esta fue una manera de solucionar la comunicaci贸n entre el robot y el PC cuando se necesitaba alg煤n dato (p. ej., el tiempo que el Duckiebot deb铆a avanzar).

+ Por 煤ltimo, dentro de `main`, se define un Loop el cual ejecuta ROS salvo que se presione el bot贸n X ya que 茅ste transforma `run = False` y por lo tanto deja de correr el programa.

Adjuntamos adem谩s en este [link](https://drive.google.com/drive/u/1/folders/1Bi4bI9MDvnyQnD3DUqhRBa8QVUB1PoVH) el Google Drive utilizado por el equipo, donde podr谩s encontar material adicional, y el informe t茅cnico y final del proyecto.



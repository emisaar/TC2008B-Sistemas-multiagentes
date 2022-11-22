# TC2008B-Sistemas-multiagentes
El respositorio contiene los archivos utilizados para la Evidencia 1.
Problemática: Modelado computacional de un sistema de Robots en un almacén.

## Parte 1. Modelado computacional en Python
Se modeló la simulación en Python con ayuda de la librería Mesa.
- Se inicializan las posiciones iniciales de las K cajas. Todas las cajas están a nivel de piso, es decir, no hay pilas de cajas. 
- Todos los agentes empiezan en posición aleatorias vacías. 
- Se ejecuta el tiempo máximo establecido. 

## Parte 2. Modelado computacional en Unity
Se modeló la simulación en Unity3D.
### Modelos con materiales (colores) y texturas (usando mapeo UV): 
- Estante (con repetición de instancias o prefabs por código).
- Caja (con repetición de instancias o prefabs por código). 
- Robot (con repetición de instancias o prefabs por código, al menos 5 robots). 
- Almacén (piso, paredes y puerta). 

### Animación 
- Los  robots  deberán  desplazarse  sobre  el  piso  del  almacén,  en  los  pasillos  que forman los estantes. 
- Para esta actividad, no es necesario conectar la simulación con el despliegue.

### Iluminación 
- Al menos una fuente de luz direccional. 
- Al  menos  una  fuente  de  luz  puntual  sobre  cada  robot  (tipo  sirena).  Dicha  luz  se 
moverá con cada robot. 

### Detección de colisiones básica 
- Los robots se moverán en rutas predeterminadas. 
- Los robots se moverán con velocidad predeterminada (aleatoria). 
- Los robots comenzarán a operar en posiciones predeterminadas (aleatorias). 
- Los robots detectarán y reaccionarán a colisiones entre ellos. Determina e implementa  un  sistema  básico  para  esto  (por  ejemplo,  detenerse  previo  a  una colisión y asignar el paso a uno de los robots). 

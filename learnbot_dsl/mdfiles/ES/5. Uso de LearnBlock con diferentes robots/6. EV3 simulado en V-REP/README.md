<a name="Init"></a>

# EV3 simulado en V-REP

El uso de la versión simulada de EV3 requiere de la instalación previa del simulador V-REP. Puede obtener las diferentes versiones disponibles de este simulador a partir del siguiente enlace [http://www.coppeliarobotics.com/](http://www.coppeliarobotics.com/) (V-REP PRO, versión recomendada: 3.6.2). Además, debe instalar los paquetes *liblua5.1-0-dev* e *inputs* mediante los siguientes comandos:

	sudo apt install liblua5.1-0-dev

	sudo pip3 install inputs

Una vez que haya instalado V-REP, necesitará descargar el fichero que contiene la versión simulada del robot (*ev3.ttt*). Dicho fichero puede obtenerse ejecutando el siguiente comando: 

	wget https://raw.githubusercontent.com/robocomp/LearnBlock/version-3/LB_add_files/ev3.ttt

Inicie V-REP y abra el fichero *ev3.ttt*. Una vez que arranque la simulación, puede ejecutar programas creados desde LearnBlock en la versión simulada de EV3. (ver la sección [Ejecutar un programa desde LearnBlock](<hidepath>/ES/4. Ejecutar un programa desde LearnBlock/README.html)).
 
[Init^](#Init)


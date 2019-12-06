<a name="Init"></a>

# Thymio

El uso de Thymio con LearnBlock requiere de la instalación previa de los paquetes *gobject* y *aseba*. Para Python3, *gobject* puede instalarse con el siguiente comando:

    sudo pip3 install PyGObject

Para instalar *aseba*, ejecute el siguiente comando:

    sudo apt-get install aseba

Debe asegurarse de que el *dongle* del robot está conectado al puerto USB de su ordenador y que el robot está encendido. Para iniciar la comunicación con el robot, ejecute el comando:

    sudo asebamedulla "ser:name=Thymio-II" 

Tras esto, puede ejecutar programas creados desde LearnBlock en el robot Thymio (ver la sección [Ejecutar un programa desde LearnBlock](<hidepath>/ES/4. Ejecutar un programa desde LearnBlock/README.html)).
 
[Init^](#Init)


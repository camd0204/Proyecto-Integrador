# Proyecto Integrador
Instalacion de RASA y codigo listo para experimentos.

### Requisitos previos

Antes de comenzar, asegurarse de tener los siguientes requisitos previos:

- Python 3.7 instalado en tu sistema.
- pip (gestor de paquetes de Python) instalado.
- Opcionalmente, considera usar un gestor de entornos virtuales como `virtualenv` para aislar el entorno de proyecto.

### Paso 1: Crear un entorno Python 3.7

Si no se esta utilizando un gestor de entornos virtuales, se puede crear el entorno `rasaENV` con Python 3.7 utilizando el siguiente comando, se debe crear el entorno :

```bash
python3.7 -m venv rasaENV
```

### Paso 2: Instalar Rasa

Dentro del entorno `rasaENV`, se isntala RASA y las dependencias usando `pip`. Ejecuta el siguiente comando:

```bash
pip install rasa
```

Este comando descargará e instalará Rasa y los paquetes necesarios.

### Paso 3: Verificar la instalación

Para verificar que Rasa se ha instalado correctamente, se comprueba la version con el siguiente comando:

```bash
rasa --version
```
.


### Paso 5: Ubicarse dentro de directorio y ejecutar servidor de acciones

Se ubica dentro de la carpeta del proyecto

```bash
cd Proyecto-Integrador
```

y posteriormente se ejecuta el comando rasa run actions, para levantar el servidor de acciones y obtener procesamiento:

```bash
rasa run actions
```
Se deja a esta ventana abierta y se puede saltar al paso 7 en una nueva ventana dentro del mismo directorio.

### Paso 6: Entrenar modelo

En caso de agregar nuevos intents se procede a usar comando train y test al modificar el nlu.yml:

```bash
rasa train
```

```bash
rasa test
```

### Paso 7: Uso del chatbot

Interaccion con el chatbot en una nueva pestana:

```bash
rasa shell
```


## Componentes de rasa
### Archivo YAML para Configuración de Red

### Resumen
Este archivo YAML define los datos de entrenamiento para un modelo de comprensión del lenguaje natural (NLU), especificando varias intenciones de usuarios relacionadas con la configuración y gestión de redes. Cada intención incluye ejemplos de consultas de usuarios relacionadas con esa acción específica.

### Categorías de Intents

(Los ejemplos estan entrenados en ingles)

#### 1. Saludos
- **Intención:** greet
  - **Ejemplos:**
    - hello
    - good day!

#### 2. Solicitar Detener Todo
- **Intención:** stop_all_request
  - **Ejemplos:**
    - I want to stop all running scenarios.
    - Stop all ongoing simulations.

#### 3. Consultar Funcionalidades
- **Intención:** ask_functionality
  - **Ejemplos:**
    - What capabilities does this bot have?
    - How can this chatbot assist me?

#### 4. Consultar Validación XML
- **Intención:** ask_xml_validation
  - **Ejemplos:**
    - Can it validate an XML configuration file?
    - Validate a VNX XML file.

#### 5. Proporcionar Ruta XML
- **Intención:** provide_xml_path
  - **Ejemplos:**
    - The file name is validationfile.
    - validationconfig is the file name.

#### 6. Solicitar Conexión de Dos Computadoras
- **Intención:** connect_two_computers_request
  - **Ejemplos:**
    - I want to connect two computers.
    - Connect two computers through a LAN.

#### 7. Consultar Escenario de Red Simple
- **Intención:** ask_simple_network_scenario
  - **Ejemplos:**
    - Can you show me an example of a simple network scenario?
    - Show an example of a simple network scenario.

#### 8. Consultar Escenario de Red Complejo
- **Intención:** ask_complex_network_scenario
  - **Ejemplos:**
    - Can you show me an example of a complex network scenario?
    - Show me an example of a complex network.

#### 9. Consultar Escenario de Red con Switch
- **Intención:** ask_switch_network_scenario
  - **Ejemplos:**
    - Can you show me an example of a network scenario with a switch?
    - Create an example with a switch for a network.

#### 10. Consultar Escenario de Switch VLAN
- **Intención:** ask_vlan_switch_scenario
  - **Ejemplos:**
    - Show me an example of a scenario that uses a VLAN.
    - Set up an example with a VLAN.

#### 11. Crear Intención de Red Personalizada
- **Intención:** create_custom_network_intent
  - **Ejemplos:**
    - I want to create a network with many users and many routers.
    - Create a network with many users and routers.

#### 12. Número de Router para Red Personalizada
- **Intención:** router_number_for_custom_network
  - **Ejemplos:**
    - 2 routers.
    - Routers for the network: 8.

#### 13. Proporcionar Usuarios por Router
- **Intención:** provide_users_per_router
  - **Ejemplos:**
    - 2 users per router.
    - Users per router: 8.

#### 14. Consultar Conceptos Básicos
- **Intención:** ask_basic_concepts
  - **Ejemplos:**
    - Tell me about a router.
    - Explain the role of a switch.

#### 15. Solicitar Conexión de Switch
- **Intención:** switch_connection_request
  - **Ejemplos:**
    - I want to connect users to a switch.
    - Create a network with a switch.

#### 16. Solicitar Configuración de Switch Cisco
- **Intención:** switch_cisco_config_request
  - **Ejemplos:**
    - I want to know the command configuration for the Cisco switch.
    - Provide the configuration for a Cisco switch.

#### 17. Proporcionar Usuarios para Switch
- **Intención:** provide_users_to_switch
  - **Ejemplos:**
    - There are 2 users for the switch.
    - Switch users: 8.

#### 18. Proporcionar Usuarios para Switch Cisco
- **Intención:** provide_users_to_cisco_switch
  - **Ejemplos:**
    - There will be 2 users for the switch.
    - Cisco switch users: 8.

#### 19. Crear Intención de Red
- **Intención:** create_network_intent
  - **Ejemplos:**
    - I want to create a virtual network with a simple router.
    - Create a network with a router.

#### 20. Preguntar Pregunta General
- **Intención:** ask_general_question
  - **Ejemplos:**
    - I want to connect a large number of users in a network, how do I proceed?
    - Show me the steps on how to create a network with many users.

#### 21. Usar Router para Conectar
- **Intención:** use_router_for_network
    - **Ejemplos:**
      - I prefer to use a router for network connectivity.
      - The chosen connectivity approach is through a router.

#### 22. Mostrar Estado del Escenario
- **Intención:** show_scenario_status
  - **Ejemplos:**
    - What is the status of the scenario?
    - Show me the status of the running scenario.

#### 23. Usar Switch para Conectar
- **Intención:** use_switch_for_networking
  - **Ejemplos:**
    - I prefer to use a switch for network connectivity.
    - The chosen connectivity approach is through a switch.

#### 24. Usar LAN para Conectar
- **Intención:** use_lan_for_networking
  - **Ejemplos:**
    - I prefer to use a LAN for network connectivity.
    - The chosen connectivity approach is through a LAN.

#### 25. Proporcionar Usuarios para la Red
- **Intención:** provide_users_to_network
  - **Ejemplos:**
    - There are 4 users connected to the router.
    - Connect 5 users using the router.

#### 26. Despedida
- **Intención:** goodbye
  - **Ejemplos:**
    - Goodbye
    - See you later
    - Until next time

#### 27. Afirmar
- **Intención:** affirm
  - **Ejemplos:**
    - Yes
    - Of course
    - Correct

#### 28. Negar
- **Intención:** deny
  - **Ejemplos:**
    - No
    - Never
    - I don't think so

#### 29. Buen Humor
- **Intención:** mood_great
  - **Ejemplos:**
    - Perfect
    - Wonderful
    - I'm great

#### 30. Mal Humor
- **Intención:** mood_unhappy
  - **Ejemplos:**
    - My day was horrible
    - I'm sad
    - I don't feel well

#### 31. Desafío del Bot
- **Intención:** bot_challenge
  - **Ejemplos:**
    - Are you a bot?
    - Am I talking to a human?

#### 32. Preguntar Diagrama de Red
- **Intención:** ask_network_diagram
  - **Ejemplos:**
    - Can you show me a network diagram?
    - Show me an example of a network diagram.

#### 33. Subir Imagen
- **Intención:** upload_image
  - **Ejemplos:**
    - I want to upload an image of a network.

#### 34. Solicitar Conexión de LAN
- **Intención:** connect_lan_request
  - **Ejemplos:**
    - I want to connect users to a LAN.
    - Use a LAN to connect users.
    - Connect users through a LAN.

#### 35. Proporcionar Usuarios para LAN
- **Intención:** provide_lan_users
  - **Ejemplos:**
    - There are [4](lan_user) users connected to the LAN.
    - Assign [3](lan_user)

### Resúmenes de Historias de Conversación

#### 1. Preguntar sobre conceptos de redes
- **Resumen:** Usuario pregunta sobre conceptos básicos de redes, sistema responde con información relevante.

#### 2. Validar archivo de configuración XML
- **Resumen:** Usuario pregunta sobre validación XML, proporciona ruta, sistema valida el archivo XML.

#### 3. Detener todos los escenarios en ejecución
- **Resumen:** Usuario solicita detener todos los escenarios en ejecución, sistema los detiene.

#### 4. Preguntar sobre el estado de un escenario de red
- **Resumen:** Usuario pregunta sobre el estado de un escenario de red, sistema responde con el estado actual.

#### 5. Mostrar diagrama de escenario
- **Resumen:** Usuario solicita ver un diagrama de escenario de red, sistema responde proporcionando el diagrama.

#### 6. Subir imagen para reconocimiento de intención
- **Resumen:** Usuario sube imagen para reconocimiento de intenciones, sistema responde proporcionando un enlace.

#### 7. Conectar dos computadoras simples
- **Resumen:** Usuario solicita conectar dos computadoras, sistema toma acciones relevantes, incluida la ejecución de un script.

#### 8. Guía para la conexión de un router
- **Resumen:** Usuario busca orientación sobre la conexión de un router, sistema proporciona instrucciones paso a paso y genera una red simple.

#### 9. Guía para la conexión de una LAN
- **Resumen:** Usuario busca orientación sobre la conexión de una LAN, sistema proporciona instrucciones y genera la configuración de la LAN.

#### 10. Guía para la conexión de un switch
- **Resumen:** Usuario busca orientación sobre la conexión de un switch, sistema proporciona instrucciones, incluida la configuración del switch.

#### 11. Crear una conexión LAN
- **Resumen:** Usuario solicita crear una conexión LAN, sistema responde pidiendo información de usuario de LAN y ejecutando un script.

#### 12. Preguntar sobre la funcionalidad del bot
- **Resumen:** Usuario saluda al bot y pregunta sobre su funcionalidad, sistema responde en consecuencia.

#### 13. Crear una red personalizada con routers y usuarios
- **Resumen:** Usuario expresa la intención de crear una red personalizada con routers y usuarios, sistema guía a través del proceso y genera la red.

#### 14. Crear una red con un switch
- **Resumen:** Usuario solicita crear una red con un switch, sistema responde pidiendo información de usuario y generando la configuración del switch.

#### 15. Generar ejemplo de configuración Cisco para switch
- **Resumen:** Usuario solicita un ejemplo de configuración Cisco para un switch, sistema responde pidiendo información de usuario y proporcionando la configuración.

#### 16. Mostrar ejemplo clásico
- **Resumen:** Usuario solicita un ejemplo de red clásico, sistema responde generando y presentando el ejemplo.

#### 17. Mostrar escenario complejo
- **Resumen:** Usuario solicita un escenario de red complejo, sistema responde generando y presentando el ejemplo.

#### 18. Mostrar ejemplo de escenario con switch
- **Resumen:** Usuario solicita un escenario de red con un switch, sistema responde generando y presentando el ejemplo.

#### 19. Mostrar ejemplo de escenario con VLAN
- **Resumen:** Usuario solicita un escenario de red con VLAN, sistema responde generando y presentando el ejemplo.

#### 20. Crear red con un router
- **Resumen:** Usuario expresa la intención de crear una red con un router, sistema responde guiando a través del proceso y generando la red.











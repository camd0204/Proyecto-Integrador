# Proyecto Integrador
## Primer avance
Avance consiste en instalacion de RASA y entrenamiento de el modelo para conceptos basicos de red

### Requisitos previos

Antes de comenzar, asegurarse de tener los siguientes requisitos previos:

- Python 3.7 instalado en tu sistema.
- pip (gestor de paquetes de Python) instalado.
- Opcionalmente, considera usar un gestor de entornos virtuales como `virtualenv` para aislar el entorno de proyecto.

### Paso 1: Crear un entorno Python 3.7

Si no se esta utilizando un gestor de entornos virtuales, se puede crear el entorno `rasaENV` con Python 3.7 utilizando el siguiente comando:

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

### Paso 4: Crear un proyecto Rasa (Opcional)

Se creo el proyecto deseadi  ejecutando el siguiente comando:

```bash
rasa init
```

Este comando guiará a el usuario través de la creación de un nuevo directorio de proyecto Rasa con los archivos y carpetas necesarios para comenzar a construir chatbots.


## Componentes de rasa
### Archivo YAML para Configuración de Red

### Resumen
Este archivo YAML define los datos de entrenamiento para un modelo de comprensión del lenguaje natural (NLU), especificando varias intenciones de usuarios relacionadas con la configuración y gestión de redes. Cada intención incluye ejemplos de consultas de usuarios relacionadas con esa acción específica.

### Categorías de Intents

#### 1. Saludos
- **Intención:** greet
  - **Ejemplos:**
    - hola
    - ¡buen día!

#### 2. Solicitar Detener Todo
- **Intención:** stop_all_request
  - **Ejemplos:**
    - Quiero detener todos los escenarios en ejecución.
    - Detener todas las simulaciones en ejecución.

#### 3. Consultar Funcionalidades
- **Intención:** ask_functionality
  - **Ejemplos:**
    - ¿Qué capacidades tiene este bot?
    - ¿Cómo puede ayudarme este chatbot?

#### 4. Consultar Validación XML
- **Intención:** ask_xml_validation
  - **Ejemplos:**
    - ¿Puede validar un archivo de configuración XML?
    - Validar un archivo XML de VNX.

#### 5. Proporcionar Ruta XML
- **Intención:** provide_xml_path
  - **Ejemplos:**
    - El nombre del archivo es [validationfile](xml_path).
    - [validationconfig](xml_path) es el nombre del archivo.

#### 6. Solicitar Conexión de Dos Computadoras
- **Intención:** connect_two_computers_request
  - **Ejemplos:**
    - Quiero conectar dos computadoras.
    - Conectar dos computadoras a través de una red LAN.

#### 7. Consultar Escenario de Red Simple
- **Intención:** ask_simple_network_scenario
  - **Ejemplos:**
    - ¿Puede mostrarme un ejemplo de un escenario de red simple?
    - muestra un ejemplo de un escenario de red simple.

#### 8. Consultar Escenario de Red Complejo
- **Intención:** ask_complex_network_scenario
  - **Ejemplos:**
    - ¿Puede mostrarme un ejemplo de un escenario de red complejo?
    - muéstrame un ejemplo de una red compleja.

#### 9. Consultar Escenario de Red con Switch
- **Intención:** ask_switch_network_scenario
  - **Ejemplos:**
    - ¿Puede mostrarme un ejemplo de un escenario de red con un switch?
    - crea un ejemplo con un switch para una red.

#### 10. Consultar Escenario de Switch VLAN
- **Intención:** ask_vlan_switch_scenario
  - **Ejemplos:**
    - Muéstrame un ejemplo de un escenario que utiliza una VLAN.
    - configura un ejemplo con una VLAN.

#### 11. Crear Intención de Red Personalizada
- **Intención:** create_custom_network_intent
  - **Ejemplos:**
    - Quiero crear una red con muchos usuarios y muchos routers.
    - crea una red con muchos usuarios y routers.

#### 12. Número de Router para Red Personalizada
- **Intención:** router_number_for_custom_network
  - **Ejemplos:**
    - [2](router_number) routers.
    - routers para la red: [8](router_number).

#### 13. Proporcionar Usuarios por Router
- **Intención:** provide_users_per_router
  - **Ejemplos:**
    - [2](user_number_for_router) usuarios por router.
    - usuarios por router: [8](user_number_for_router).

#### 14. Consultar Conceptos Básicos
- **Intención:** ask_basic_concepts
  - **Ejemplos:**
    - Cuéntame sobre un [router](network_device).
    - Explica el papel de un [switch](network_device).

#### 15. Solicitar Conexión de Switch
- **Intención:** switch_connection_request
  - **Ejemplos:**
    - Quiero conectar usuarios a un switch.
    - haz una red con un switch.

#### 16. Solicitar Configuración de Switch Cisco
- **Intención:** switch_cisco_config_request
  - **Ejemplos:**
    - Quiero conocer la configuración de comandos del switch Cisco.
    - proporciona la configuración para un switch Cisco.

#### 17. Proporcionar Usuarios para Switch
- **Intención:** provide_users_to_switch
  - **Ejemplos:**
    - Hay [2](user_number) usuarios para el switch.
    - Usuarios de switch: [8](user_number).

#### 18. Proporcionar Usuarios para Switch Cisco
- **Intención:** provide_users_to_cisco_switch
  - **Ejemplos:**
    - Habrá [2](user_number_cisco) usuarios para el switch.
    - Usuarios de switch Cisco: [8](user_number_cisco).

#### 19. Crear Intención de Red
- **Intención:** create_network_intent
  - **Ejemplos:**
    - Quiero crear una red virtual con un router simple.
    - crea una red con un router.

#### 20. Preguntar Pregunta General
- **Intención:** ask_general_question
  - **Ejemplos:**
    - Quiero conectar a un gran número de usuarios en una red, ¿cómo procedo?
    - muéstrame los pasos sobre cómo crear una red con muchos usuarios.

#### 21. Usar Router para Conectar
- **Intención:** use_router_for_network
    - **Ejemplos:**
      - Prefiero usar un router para la conectividad de red.
      - El enfoque de conectividad elegido es mediante un router.

#### 22. Mostrar Estado del Escenario
- **Intención:** show_scenario_status
  - **Ejemplos:**
    - ¿Cuál es el estado del escenario?
    - Muéstrame el estado del escenario en ejecución.

#### 23. Usar Switch para Conectar
- **Intención:** use_switch_for_networking
  - **Ejemplos:**
    - Prefiero usar un switch para la conectividad de red.
    - El enfoque de conectividad elegido es mediante un switch.

#### 24. Usar LAN para Conectar
- **Intención:** use_lan_for_networking
  - **Ejemplos:**
    - Prefiero usar una LAN para la conectividad de red.
    - El enfoque de conectividad elegido es mediante una LAN.

#### 25. Proporcionar Usuarios para la Red
- **Intención:** provide_users_to_network
  - **Ejemplos:**
    - Hay [4](user_number_n) usuarios conectados al router.
    - Conectar [5](user_number_n) usuarios usando el router.

#### 26. Despedida
- **Intención:** goodbye
  - **Ejemplos:**
    - Adiós
    - Hasta luego
    - Nos vemos

#### 27. Afirmar
- **Intención:** affirm
  - **Ejemplos:**
    - Sí
    - Por supuesto
    - Correcto

#### 28. Negar
- **Intención:** deny
  - **Ejemplos:**
    - No
    - Nunca
    - No creo que sí

#### 29. Buen Humor
- **Intención:** mood_great
  - **Ejemplos:**
    - Perfecto
    - Maravilloso
    - Estoy genial

#### 30. Mal Humor
- **Intención:** mood_unhappy
  - **Ejemplos:**
    - Mi día fue horrible
    - Estoy triste
    - No me siento bien

#### 31. Desafío del Bot
- **Intención:** bot_challenge
  - **Ejemplos:**
    - ¿Eres un bot?
    - ¿Estoy hablando con un humano?

#### 32. Preguntar Diagrama de Red
- **Intención:** ask_network_diagram
  - **Ejemplos:**
    - ¿Puedes mostrarme un diagrama de red?
    - Muéstrame un ejemplo de un diagrama de red.

#### 33. Subir Imagen
- **Intención:** upload_image
  - **Ejemplos:**
    - Quiero subir una imagen de una red.

#### 34. Solicitar Conexión de LAN
- **Intención:** connect_lan_request
  - **Ejemplos:**
    - Quiero conectar usuarios a una red LAN.
    - Utilizar una red LAN para conectar usuarios.
    - Conectar usuarios mediante una red LAN.

#### 35. Proporcionar Usuarios para LAN
- **Intención:** provide_lan_users
  - **Ejemplos:**
    - Hay [4](lan_user) usuarios conectados a la LAN.
    - Asignar [3](lan_user) usuarios a la LAN.


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











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




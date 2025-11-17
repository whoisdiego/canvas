# Canvas

Canvas es un conjunto de scripts en Python y Bash diseñado para facilitar la gestión y entrega de tareas en la plataforma Experiencia21 del Tecnológico de Monterrey.  
Permite a los estudiantes listar sus tareas pendientes, automatizar la subida de archivos y manejar el flujo de entrega directamente desde la terminal.

## Requisitos

- Python 3.10 o superior  
- Bash (Git Bash o WSL en Windows)  
- Módulos de Python: `requests`, `beautifulsoup4`, `pycryptodome`, `pywin32`  
- Google Chrome con sesión activa en Experiencia21  
- Ejecutar con privilegios de administrador para permitir el uso de Shadow Copy  
- Windows

## Instalación
  Clona el repositorio y navega a la carpeta del proyecto. 
  
    git clone https://github.com/whoisdiego/canvas.git
Agrega el proyecto al PATH para poder ejecutar canvas desde cualquier ubicación y en cualquier sesión.

O copia y pega estas linea en el bash para que se guarde en el archivo bashrc, que se ejecuta cada vez que abres una shell, la accion de agregar al path canvas.

    echo 'export PATH="$PATH:/ruta/al/proyecto/canvas"' >> ~/.bashrc

  - Instalar autocompletado. Esto habilita TAB para sugerencias en el comando canvas. Debes de estar en el directorio donde se ubica 
  
        echo "source $(pwd)/canvas.sh" >> ~/.bashrc
    
        // Para ver los cambios en la misma shell
    
        source ~/.bashrc

## Uso

### Mostrar las tareas disponibles
Lista todas las tareas obtenidas desde `bash_tareas.py`.


    canvas show
      ACT1
      ACT2
      ACT3

### Ver ayuda del comando

Muestra los comandos disponibles y su forma de uso.

    post     manda la tarea. Uso--canvas post 'nombre_elegido' 'tarea2' 'nombre_del_archivo.pdf' 'nombre_del_archivo2.cpp'
    show     muestra las tareas por hacer. Uso--canvas show
    help     muestra los comandos

### Enviar una tarea con varios archivos

Dependiendo de cuántos archivos se ingresen, se crea un archivo ZIP. Si se ingresa un solo archivo, se envía ese archivo directamente. Si se ingresan dos o más archivos, se crea un ZIP con estos dentro.

    canvas post "nombre_final" "nombre_de_tarea" archivo1.pdf archivo2.cpp archivo3.png
Si el envio fue exitoso regresa

    Se mando la tarea
Si hubo error

    No se mando la tarea. Status diferente de 200

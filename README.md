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

  - Instalar autocompletado en Bash. Esto habilita TAB para sugerencias en el comando canvas.
  
        echo "source $(pwd)/devtool_completion.sh" >> ~/.bashrc
        source ~/.bashrc


  


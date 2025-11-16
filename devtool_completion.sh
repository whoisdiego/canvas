#!/bin/bash

# Ejecuta Python y convierte la salida (líneas) en un array real
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readarray -t TAREAS < <(python "$SCRIPT_DIR/bash_tareas.py")
FILES="$(ls)"

function canvas {
  local WAD="$1"
  local FILE_NAMES=()
  if [ $# -eq 1 ]; then
    case "$1" in 
      help)
        echo -e "post     manda la tarea. Uso--canvas post 'nombre_elegido' 'tarea2' 'nombre_del_archivo.pdf'\nshow     muestra las tareas por hacer. Uso--canvas show\nhelp     muestra los comandos"
        ;;
      show)
        printf "%s\n" "${TAREAS[@]}"
        ;;
    esac
  elif [[ "$WAD" == "post" && "$#" -ge 4 ]]; then
    local CHOSEN_NAME="$2"
    local ASSIGNMENT="$3"
    FILES_NAMES=()
    for ((i=4; i<=$#; i++)); do
      FILE="${!i}"
      if ! compgen -W "$FILES" -- "${FILE}" > /dev/null; then
        echo "No exites el archivo ${!i}"
        exit 0
      else
        FILES_NAMES+=("$FILE")
      fi
    done

    if [[ "${#FILES_NAMES[@]}" -gt 1 ]]; then
      zip -rq "${CHOSEN_NAME}.zip" "${FILES_NAMES[@]}"
      STATUS="$(python post_tarea.py "${CHOSEN_NAME}.zip" "$ASSIGNMENT")"
      printf "%s\n" "${STATUS[@]}"
    else
      extension="${FILES_NAMES##*.}"
      STATUS="$(python post_tarea.py "${CHOSEN_NAME}${extension}" "$ASSIGNMENT")"
      printf "%s\n" "${STATUS[@]}"
    fi
  else
    echo "Sintaxis Incorrecta"
  fi
}

function _canvas {
  local AVAILABLE="help show post"
  local CURRENT_WORD="${COMP_WORDS[$COMP_CWORD]}"
  local WAD=${COMP_WORDS[1]}


  if [ "$COMP_CWORD" -eq 1 ]; then
    COMPREPLY=($(compgen -W "$AVAILABLE" -- "$CURRENT_WORD"))

  elif [[ "$COMP_CWORD" -eq 3 && "${COMP_WORDS[1]}" == "post" ]]; then
    COMPREPLY=($(compgen -W "${TAREAS[*]}" -- "$CURRENT_WORD"))

  elif [[ "post" == "$WAD" && "$COMP_CWORD" -gt 3 ]]; then
    COMPREPLY=($(compgen -W "$FILES" -- "$CURRENT_WORD"))
  fi

}

complete -F _canvas canvas

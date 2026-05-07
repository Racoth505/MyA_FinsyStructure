#!/bin/bash

# Validar si se ejecuta como root
if [ "$EUID" -ne 0 ]; then 
  echo "Por favor, ejecuta como sudo: sudo ./cleanup_logs.sh"
  exit
fi

echo "--- Iniciando limpieza de logs antiguos (más de 7 días) ---"

# -mtime +7 busca archivos modificados hace más de 7 días
# Se añade redirección de errores a /dev/null para evitar mensajes de carpetas protegidas
find /var/log -type f -name "*.log" -mtime +7 -exec rm -f {} \; 2>/dev/null

echo "Limpieza completada: $(date)"
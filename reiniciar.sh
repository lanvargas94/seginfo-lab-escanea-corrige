#!/usr/bin/env bash
# Enciende el servidor, o lo reinicia para que tome los cambios de configuracion.
docker compose up -d --build --force-recreate
sleep 2
echo
docker compose ps --format 'table {{.Service}}\t{{.State}}'
echo
if [ "$(docker compose ps --status running -q | wc -l)" -lt 3 ]; then
  echo "OJO: algun servicio no quedo encendido. Mire el error con: docker compose logs"
else
  echo "Listo: los 3 servicios estan encendidos."
fi

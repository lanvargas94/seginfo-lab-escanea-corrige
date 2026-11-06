#!/usr/bin/env bash
# Enciende el servidor, o lo reinicia para que tome los cambios de configuracion.
docker compose up -d --build --force-recreate
sleep 3
echo
docker compose ps -a --format 'table {{.Service}}\t{{.State}}'
echo
FALLAN="$(docker compose ps -a --format '{{.Service}} {{.State}}' | grep -v ' running$' | cut -d' ' -f1 | tr '\n' ' ')"
if [ -n "$FALLAN" ]; then
  echo "OJO: no quedo encendido: $FALLAN"
  echo "Mire el error con: docker compose logs"
else
  echo "Listo: los 3 servicios estan encendidos."
fi

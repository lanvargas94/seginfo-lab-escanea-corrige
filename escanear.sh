#!/usr/bin/env bash
# Uso: ./escanear.sh antes   o   ./escanear.sh despues
ETAPA="${1:-antes}"
mkdir -p evidencia
SALIDA="evidencia/escaneo_${ETAPA}.txt"
{
  echo "=== Escaneo ${ETAPA} - usuario: ${GITHUB_USER:-local} - $(date -u '+%Y-%m-%d %H:%M UTC') ==="
  echo
  echo "--- Nmap: puertos, servicios y scripts basicos ---"
  nmap -Pn -sV -sC -p 2121,6379,8080 127.0.0.1
  echo
  echo "--- Nuclei: fallas conocidas en la web ---"
  nuclei -u http://127.0.0.1:8080 -tags exposure,config,misconfig,listing,panel,git -no-color -silent -duc -timeout 5 -rl 100
} 2>&1 | tee "$SALIDA"
echo
echo "Resultado guardado en: $SALIDA"

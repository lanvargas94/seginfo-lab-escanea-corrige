#!/usr/bin/env bash
# Instala Nmap y Nuclei. Se ejecuta una sola vez, al abrir el Codespace.
set -e
NUCLEI_VERSION="3.3.10"
echo "Instalando Nmap..."
# La imagen de Codespaces trae un repositorio de Yarn con firma vencida; aqui no se necesita.
sudo rm -f /etc/apt/sources.list.d/yarn.list
sudo apt-get update -qq
sudo apt-get install -y -qq nmap unzip >/dev/null
echo "Instalando Nuclei..."
curl -fsSL -o /tmp/nuclei.zip "https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip"
sudo unzip -oq /tmp/nuclei.zip nuclei -d /usr/local/bin
echo "Descargando plantillas de Nuclei..."
nuclei -update-templates -silent -duc || true
chmod +x reiniciar.sh escanear.sh verificar.py
nmap --version | head -1
nuclei -version 2>&1 | tail -1
echo "Herramientas listas."

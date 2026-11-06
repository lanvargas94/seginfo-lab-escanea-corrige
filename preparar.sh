#!/usr/bin/env bash
# Se ejecuta una sola vez, cuando se crea el Codespace. Instala Nmap y Nuclei.
set -e
NUCLEI_VERSION="3.3.10"
sudo apt-get update -qq
sudo apt-get install -y -qq nmap unzip >/dev/null
curl -fsSL -o /tmp/nuclei.zip "https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip"
sudo unzip -oq /tmp/nuclei.zip nuclei -d /usr/local/bin
nuclei -update-templates -silent -duc || true
chmod +x reiniciar.sh escanear.sh verificar.py
echo "Herramientas listas."

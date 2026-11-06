# Laboratorio: escanea, corrige y demuéstralo

Práctica de Seguridad de la Información (CORHUILA, 2026-B). Este repositorio contiene un servidor **vulnerable a propósito** y con **datos inventados**. Solo debe ejecutarse dentro de su propio Codespace. No lo despliegue en un servidor público.

## Inicio rápido

1. Botón verde **Code → Codespaces → Create codespace on main**.
2. Espere a que termine la preparación y, en la terminal:

```bash
./reiniciar.sh            # enciende el servidor
./escanear.sh antes       # primer escaneo
python3 verificar.py      # qué fallas siguen abiertas
```

3. Corrija los archivos dentro de `servidor/`, ejecute `./reiniciar.sh` y vuelva a verificar.
4. Al terminar: `./escanear.sh despues`.

La guía completa está en Moodle. Al terminar, detenga su Codespace para no gastar su cuota gratuita.

#!/usr/bin/env python3
"""Comprueba, desde afuera, que fallas siguen abiertas en el servidor del laboratorio."""
import datetime
import ftplib
import http.client
import os
import re
import socket

HOST = "127.0.0.1"
PUERTO_WEB = 8080
PUERTO_REDIS = 6379
PUERTO_FTP = 2121


def pedir(ruta):
    """Devuelve (estado, cabeceras en minuscula, cuerpo) o None si la web no responde."""
    try:
        conexion = http.client.HTTPConnection(HOST, PUERTO_WEB, timeout=5)
        conexion.request("GET", ruta)
        respuesta = conexion.getresponse()
        cuerpo = respuesta.read().decode("utf-8", "replace")
        cabeceras = {k.lower(): v for k, v in respuesta.getheaders()}
        conexion.close()
        return respuesta.status, cabeceras, cuerpo
    except OSError:
        return None


def web_viva():
    r = pedir("/")
    return r is not None and r[0] == 200 and "Tienda Opita" in r[2]


def f1_env():
    r = pedir("/.env")
    return "DB_PASSWORD" not in r[2]


def f2_git():
    r = pedir("/.git/config")
    return "[remote" not in r[2] and "[core]" not in r[2]


def f3_listado():
    r = pedir("/backup/")
    return "clientes_2026.sql" not in r[2] and "Index of" not in r[2]


def f4_admin():
    r = pedir("/admin/")
    return r[0] in (401, 403)


def f5_version():
    r = pedir("/")
    return not re.search(r"\d", r[1].get("server", ""))


def f6_cabeceras():
    r = pedir("/")
    return (
        r[1].get("x-content-type-options", "").lower() == "nosniff"
        and r[1].get("x-frame-options", "").upper() in ("DENY", "SAMEORIGIN")
        and bool(r[1].get("content-security-policy"))
    )


def f7_redis():
    """None = servicio apagado. True = pide contrasena. False = abierto."""
    try:
        with socket.create_connection((HOST, PUERTO_REDIS), timeout=5) as s:
            s.sendall(b"PING\r\n")
            s.settimeout(5)
            datos = s.recv(200)
    except OSError:
        return None
    if not datos:
        return None
    if datos.startswith(b"+PONG"):
        return False
    return b"NOAUTH" in datos


def f8_ftp():
    """None = servicio apagado. True = rechaza anonimo. False = lo acepta."""
    try:
        ftp = ftplib.FTP()
        ftp.connect(HOST, PUERTO_FTP, timeout=5)
    except (OSError, EOFError, ftplib.Error):
        return None
    try:
        ftp.login("anonymous", "lab@lab.example")
        ftp.quit()
        return False
    except ftplib.error_perm:
        return True
    except (OSError, EOFError, ftplib.Error):
        return None


def main():
    print("=" * 62)
    print(" VERIFICADOR DEL LABORATORIO - Tienda Opita")
    print(" Usuario : " + os.environ.get("GITHUB_USER", "(sin usuario)"))
    print(" Codespace: " + os.environ.get("CODESPACE_NAME", "(local)"))
    print(" Fecha UTC: " + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 62)

    viva = web_viva()
    if not viva:
        print(" [!!] La pagina principal de la tienda NO responde.")
        print("      Las 6 fallas web no cuentan: apagar la tienda no es corregirla.")
        print("      Mire el error con: docker compose logs web")

    pruebas = [
        ("F1", "Archivo .env con contrasenas a la vista", f1_env if viva else None),
        ("F2", "Carpeta .git publicada", f2_git if viva else None),
        ("F3", "Listado de la carpeta /backup/", f3_listado if viva else None),
        ("F4", "Panel /admin/ sin autenticacion", f4_admin if viva else None),
        ("F5", "El servidor revela su version", f5_version if viva else None),
        ("F6", "Faltan cabeceras de seguridad", f6_cabeceras if viva else None),
        ("F7", "Redis sin contrasena", f7_redis),
        ("F8", "FTP con acceso anonimo", f8_ftp),
    ]

    corregidas = 0
    for codigo, nombre, prueba in pruebas:
        resultado = prueba() if prueba else None
        if resultado is True:
            corregidas += 1
            marca = "CORREGIDA"
        elif resultado is False:
            marca = "ABIERTA  "
        else:
            marca = "APAGADA  "
        print(f" {marca} {codigo}  {nombre}")

    print("-" * 62)
    print(f" Fallas corregidas: {corregidas} de 8  (se piden al menos 5)")
    if corregidas >= 5:
        print(" Meta cumplida. Tome captura de esta pantalla completa.")
    print("=" * 62)


if __name__ == "__main__":
    main()

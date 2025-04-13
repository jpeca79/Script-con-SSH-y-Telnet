# Auditoría SSH y Telnet con Shodan

Esta herramienta realiza una auditoría automatizada sobre servicios SSH y Telnet expuestos en Internet. Usa la API de Shodan para buscar dispositivos vulnerables y verifica acceso con combinaciones de usuario y contraseña desde archivos de texto.

Incluye dos modos de uso:
- Interfaz de línea de comandos (CLI)
- Interfaz gráfica de usuario (GUI) con Tkinter

---

REQUISITOS
----------
- Python 3.8 o superior
- Módulos: shodan, paramiko, telnetlib3, asyncio, tkinter (nativo)
- Conexión a Internet
- Cuenta Shodan con API Key

---

INSTALACIÓN
-----------
1. Crear entorno virtual (opcional):
   - Windows:
     python -m venv venv
     venv\Scripts\activate

   - Linux:
     python3 -m venv venv
     source venv/bin/activate

2. Instalar dependencias:
   pip install shodan paramiko telnetlib3

3. Crear archivos:
   - usuarios.txt → una lista de usuarios (uno por línea)
   - passwords.txt → una lista de contraseñas (uno por línea)

4. En el archivo auditor.py, agregar tu API Key de Shodan:
   API_KEY = 'TU_API_KEY_AQUI'

---

EJECUCIÓN
---------

MODO CONSOLA (CLI):
   python auditor.py

MODO INTERFAZ GRÁFICA (GUI):
   python gui.py

Desde la GUI podés iniciar la auditoría con un botón y ver los resultados en tiempo real en pantalla.

---

FUNCIONALIDAD
-------------
- Busca IPs en Shodan con puertos 22 (SSH) y 23 (Telnet)
- Limita resultados a países de Latinoamérica
- Prueba accesos con usuarios/contraseñas desde archivos .txt
- Registra los accesos exitosos en lista_ips.txt con fecha, IP y credenciales

---

EJEMPLO DE RESULTADO EN lista_ips.txt
-------------------------------------
[2025-04-10 15:22:34] SSH - 190.12.34.56 (root/admin)
[2025-04-10 15:25:10] TELNET - 181.22.15.33 (admin/1234)

---

ADVERTENCIA LEGAL
-----------------
Este proyecto es para fines académicos y educativos. No debe utilizarse para comprometer sistemas ajenos sin permiso explícito. El mal uso puede tener consecuencias legales.

---

LICENCIA
--------
MIT License – Uso libre con atribución.


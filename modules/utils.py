from datetime import datetime
from config import SHODAN_API_KEY  # 🔑 Importar la API key

def cargar_api_key():
    return SHODAN_API_KEY

def cargar_lista(ruta):
    with open(ruta, "r") as f:
        return [line.strip() for line in f if line.strip()]

def guardar_vulnerable(ip, servicio, usuario, clave):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("lista_ips.txt", "a") as f:
        f.write(f"[{timestamp}] {servicio.upper()} - {ip} ({usuario}/{clave})\n")

def log_error(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("errores.log", "a") as f:
        f.write(f"[{timestamp}] {mensaje}\n")

def log_estadisticas(total_ssh, exitosos_ssh, total_telnet, exitosos_telnet):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("estadisticas.log", "a") as f:
        f.write(f"[{timestamp}] SSH: {exitosos_ssh}/{total_ssh} ({(exitosos_ssh / total_ssh * 100) if total_ssh else 0:.2f}%) | ")
        f.write(f"Telnet: {exitosos_telnet}/{total_telnet} ({(exitosos_telnet / total_telnet * 100) if total_telnet else 0:.2f}%)\n")

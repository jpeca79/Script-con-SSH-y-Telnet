import asyncio
import telnetlib3
from modules.utils import guardar_vulnerable, cargar_lista

async def verificar_telnet_ip(ip, usuarios, passwords):
    for usuario in usuarios:
        for clave in passwords:
            try:
                reader, writer = await asyncio.wait_for(
                    telnetlib3.open_connection(ip, 23),
                    timeout=5
                )

                await reader.readuntil("login: ")
                writer.write(usuario + "\n")
                await reader.readuntil("Password: ")
                writer.write(clave + "\n")

                response = await reader.read(100)
                if "incorrect" not in response.lower():
                    print(f"[+] Telnet acceso exitoso: {ip} ({usuario}/{clave})")
                    guardar_vulnerable(ip, "telnet", usuario, clave)
                    writer.close()
                    return True
                else:
                    writer.close()
            except Exception:
                continue
    print(f"[-] Telnet falló: {ip}")
    return False

async def verificar_telnet(lista_ips):
    usuarios = cargar_lista("usuarios.txt")
    passwords = cargar_lista("passwords.txt")

    tareas = [verificar_telnet_ip(ip, usuarios, passwords) for ip in lista_ips]
    resultados = await asyncio.gather(*tareas)
    return sum(1 for r in resultados if r)


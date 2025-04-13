import shodan
from modules.utils import cargar_api_key
from config import PAISES_LATAM
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

lock = threading.Lock()  # Para proteger acceso a listas compartidas

def buscar_en_pais(api, pais, dispositivos_ssh, dispositivos_telnet):
    try:
        print(f"[*] Buscando en {pais}...")

        resultados_ssh = api.search(f'port:22 country:{pais}')
        resultados_telnet = api.search(f'port:23 country:{pais}')

        with lock:
            for servicio in resultados_ssh['matches']:
                dispositivos_ssh.append(servicio['ip_str'])

            for servicio in resultados_telnet['matches']:
                dispositivos_telnet.append(servicio['ip_str'])

    except Exception as e:
        print(f"[!] Error con {pais}: {e}")

def buscar_dispositivos():
    api_key = cargar_api_key()
    api = shodan.Shodan(api_key)
    dispositivos_ssh = []
    dispositivos_telnet = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(buscar_en_pais, api, pais, dispositivos_ssh, dispositivos_telnet) for pais in PAISES_LATAM]

        # Esperamos hasta 5 minutos como máximo
        for future in as_completed(futures, timeout=300):
            try:
                future.result()
            except Exception:
                continue

    return dispositivos_ssh, dispositivos_telnet

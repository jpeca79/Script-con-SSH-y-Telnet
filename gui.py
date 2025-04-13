import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import auditor  # importa tu script existente

# Función para mostrar mensajes en la GUI y en consola
def mostrar_en_gui(texto):
    log_text.insert(tk.END, texto + "\n")
    log_text.see(tk.END)  # Desplaza hacia el final automáticamente
    print(texto)  # También lo muestra en terminal

# Ejecutar la auditoría en un hilo separado para no congelar la GUI
def ejecutar_en_hilo():
    btn.config(state="disabled")
    mostrar_en_gui("[*] Ejecutando auditoría...")
    threading.Thread(target=lambda: asyncio.run(ejecutar_gui())).start()

# Función que corre la auditoría
async def ejecutar_gui():
    try:
        auditor.print_gui = mostrar_en_gui  # Redirigir logs desde auditor.py a GUI
        await auditor.ejecutar_auditoria()
        mostrar_en_gui("[✓] Auditoría finalizada.")
    except Exception as e:
        mostrar_en_gui(f"[!] Error: {e}")
    finally:
        btn.config(state="normal")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Auditoría SSH y Telnet")
ventana.geometry("600x400")

# Estilo visual moderno
style = ttk.Style()
style.theme_use("clam")

# Botón para lanzar auditoría
btn = ttk.Button(ventana, text="Iniciar Auditoría", command=ejecutar_en_hilo)
btn.pack(pady=10)

# Cuadro de texto para logs
log_text = tk.Text(ventana, wrap=tk.WORD, height=20)
log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Iniciar loop gráfico
ventana.mainloop()

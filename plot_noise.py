import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==========================================
# CONFIGURACIÓN
# ==========================================
NOMBRE_ARCHIVO = "eclipse_ruido_29MHz.csv"  # Asegúrate de coincidir con el CSV generado

# Si quieres marcar los contactos del eclipse, rellena estas horas (formato "HH:MM:SS")
# y pon MOSTRAR_CONTACTOS = True. Si no las conoces, déjalo en False.
MOSTRAR_CONTACTOS = False
FECHA_ECLIPSE = "2026-08-12"  # ajusta a la fecha real de tu observación
CONTACTOS = {
    "C1 (inicio)": "17:30:00",
    "Máximo": "18:45:00",
    "C4 (fin)": "20:00:00",
}

# Umbral: si entre dos muestras consecutivas pasa más tiempo que
# INTERVALO_ESPERADO_SEC * TOLERANCIA, se considera un hueco de datos
INTERVALO_ESPERADO_SEC = 2
TOLERANCIA = 3

# ==========================================
# 1. Cargar y validar los datos
# ==========================================
if not os.path.exists(NOMBRE_ARCHIVO):
    sys.exit(f"[!] No se encontró el archivo '{NOMBRE_ARCHIVO}'.")

df = pd.read_csv(NOMBRE_ARCHIVO)

if df.empty:
    sys.exit(f"[!] El archivo '{NOMBRE_ARCHIVO}' no contiene datos.")

df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

print(f"[+] {len(df)} muestras cargadas, desde {df['timestamp'].min()} hasta {df['timestamp'].max()}")

# ==========================================
# 2. Detectar huecos de datos y romper la línea ahí
#    (para no conectar visualmente intervalos sin medición real)
# ==========================================
gaps = df['timestamp'].diff().dt.total_seconds() > (INTERVALO_ESPERADO_SEC * TOLERANCIA)
n_huecos = int(gaps.sum())
if n_huecos > 0:
    print(f"[!] Se detectaron {n_huecos} huecos de datos; no se conectarán con línea recta.")

df_plot = df.copy()
df_plot.loc[gaps, 'power_dB'] = np.nan  # NaN corta la línea en matplotlib

# ==========================================
# 3. Configurar la figura
# ==========================================
plt.figure(figsize=(12, 6))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# 4. Dibujar la curva de potencia
plt.plot(df_plot['timestamp'], df_plot['power_dB'], color='#e67e22', linewidth=1.2, label='Piso de ruido (29 MHz)')

# 4b. Marcar huecos de datos como zonas sombreadas (opcional pero útil para el alumnado)
if n_huecos > 0:
    for idx in df.index[gaps]:
        plt.axvspan(df['timestamp'][idx - 1], df['timestamp'][idx], color='gray', alpha=0.15)

# 4c. Marcar contactos del eclipse si se han indicado
if MOSTRAR_CONTACTOS:
    for etiqueta, hora in CONTACTOS.items():
        t = pd.to_datetime(f"{FECHA_ECLIPSE} {hora}")
        plt.axvline(t, color='#2c3e50', linestyle='--', linewidth=1)
        plt.text(t, plt.ylim()[1], etiqueta, rotation=90, va='top', ha='right', fontsize=9)

# 5. Formato de títulos y ejes
plt.title("Evolución del Piso de Ruido Solar/Ionosférico en 29.0 MHz", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Hora Local (CEST)", fontsize=11, labelpad=10)
plt.ylabel("Potencia de Ruido Relativa (dB)", fontsize=11)

# 6. Formatear las horas en el eje X para que no se amontonen
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=30, ha='right')

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right')
plt.tight_layout()

# 7. Guardar y mostrar la gráfica
plt.savefig("grafica_eclipse_29MHz.png", dpi=300)
print("¡Gráfica guardada exitosamente como 'grafica_eclipse_29MHz.png'!")
plt.show()

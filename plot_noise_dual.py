# Software developed by EA5JTT for display of solar noise file
#in CSV format.
#
# Copyright (C) 2026 Juan Pablo Sanchez EA5JTT
# =================================================================
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==========================================
# CONFIGURACIÓN
# ==========================================
ARCHIVO_REFERENCIA = "ruido_29MHz_20260725_100818.csv"  # día anterior, sin eclipse
ARCHIVO_ECLIPSE    = "ruido_29MHz_20260726_100818.csv"  # día del eclipse

ETIQUETA_REFERENCIA = "Día anterior (referencia)"
ETIQUETA_ECLIPSE = "Día del eclipse"

# Si quieres marcar los contactos del eclipse, rellena estas horas (formato "HH:MM:SS")
# y pon MOSTRAR_CONTACTOS = True. Si no las conoces, déjalo en False.
MOSTRAR_CONTACTOS = False
CONTACTOS = {
    "C1 (inicio)": "17:30:00",
    "Máximo": "18:45:00",
    "C4 (fin)": "20:00:00",
}

# Umbral: si entre dos muestras consecutivas pasa más tiempo que
# INTERVALO_ESPERADO_SEC * TOLERANCIA, se considera un hueco de datos
INTERVALO_ESPERADO_SEC = 2
TOLERANCIA = 3


def cargar_serie(nombre_archivo, etiqueta):
    """Carga un CSV de ruido, valida su contenido y normaliza el eje temporal
    a 'hora del día' (fecha de referencia arbitraria 1900-01-01) para poder
    superponerlo con series de otras fechas."""
    if not os.path.exists(nombre_archivo):
        sys.exit(f"[!] No se encontró el archivo '{nombre_archivo}' ({etiqueta}).")

    df = pd.read_csv(nombre_archivo)
    if df.empty:
        sys.exit(f"[!] El archivo '{nombre_archivo}' no contiene datos ({etiqueta}).")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    print(f"[+] {etiqueta}: {len(df)} muestras, desde {df['timestamp'].min()} hasta {df['timestamp'].max()}")

    # Detectar huecos de datos (antes de normalizar la fecha)
    gaps = df['timestamp'].diff().dt.total_seconds() > (INTERVALO_ESPERADO_SEC * TOLERANCIA)
    n_huecos = int(gaps.sum())
    if n_huecos > 0:
        print(f"[!] {etiqueta}: se detectaron {n_huecos} huecos de datos; no se conectarán con línea recta.")

    df['power_dB_plot'] = df['power_dB']
    df.loc[gaps, 'power_dB_plot'] = np.nan  # NaN corta la línea en matplotlib

    # Normalizar: nos quedamos solo con la hora del día, sobre una fecha común ficticia
    # (1900-01-01), para que dos días distintos se superpongan en el mismo eje X
    hora_del_dia = df['timestamp'].dt.time
    df['tiempo_normalizado'] = pd.to_datetime(
        hora_del_dia.astype(str), format='%H:%M:%S'
    )

    return df


# ==========================================
# 1. Cargar y validar los dos ficheros
# ==========================================
df_ref = cargar_serie(ARCHIVO_REFERENCIA, ETIQUETA_REFERENCIA)
df_ecl = cargar_serie(ARCHIVO_ECLIPSE, ETIQUETA_ECLIPSE)

# ==========================================
# 2. Configurar la figura
# ==========================================
plt.figure(figsize=(12, 6))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# 3. Dibujar ambas curvas sobre el mismo eje de "hora del día"
plt.plot(df_ref['tiempo_normalizado'], df_ref['power_dB_plot'],
         color='#3498db', linewidth=1.2, label=ETIQUETA_REFERENCIA)
plt.plot(df_ecl['tiempo_normalizado'], df_ecl['power_dB_plot'],
         color='#e67e22', linewidth=1.2, label=ETIQUETA_ECLIPSE)

# 4. Marcar contactos del eclipse si se han indicado (solo hora, sobre la fecha ficticia)
if MOSTRAR_CONTACTOS:
    for etiqueta, hora in CONTACTOS.items():
        t = pd.to_datetime(hora, format='%H:%M:%S')
        plt.axvline(t, color='#2c3e50', linestyle='--', linewidth=1)
        plt.text(t, plt.ylim()[1], etiqueta, rotation=90, va='top', ha='right', fontsize=9)

# 5. Formato de títulos y ejes
plt.title("Comparativa del Piso de Ruido Solar/Ionosférico en 29.0 MHz\nDía de referencia vs Día del eclipse",
          fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Hora del Día (CEST)", fontsize=11, labelpad=10)
plt.ylabel("Potencia de Ruido Relativa (dB)", fontsize=11)

# 6. Formatear las horas en el eje X para que no se amontonen
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=30, ha='right')

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right')
plt.tight_layout()

# 7. Guardar y mostrar la gráfica
plt.savefig("grafica_comparativa_eclipse_29MHz.png", dpi=300)
print("¡Gráfica guardada exitosamente como 'grafica_comparativa_eclipse_29MHz.png'!")
plt.show()

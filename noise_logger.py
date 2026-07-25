import ctypes

# Parche global para bibliotecas librtlsdr antiguas en macOS / Python 3.14
_original_getitem = ctypes.CDLL.__getitem__

def _patched_getitem(self, name_or_ordinal):
    try:
        return _original_getitem(self, name_or_ordinal)
    except AttributeError:
        # Si la función C no existe en el sistema, devuelve una función dummy que no rompe el programa
        return ctypes.CFUNCTYPE(ctypes.c_int)(lambda *args: 0)

ctypes.CDLL.__getitem__ = _patched_getitem

import csv











import csv
import time
import numpy as np
from rtlsdr import RtlSdr

# ==========================================
# CONFIGURACIÓN DEL EXPERIMENTO
# ==========================================
FRECUENCIA_HZ = 29.0e6      # 29.0 MHz
SAMPLE_RATE = 1.0e6         # 1.0 MS/s
GAIN_DB = 25.4              # Ganancia fija en dB
INTERVALO_SEC = 2           # Medición cada 2 segundos
DURACION_HORAS = 2.5        # Tiempo total
NOMBRE_ARCHIVO = "eclipse_ruido_29MHz.csv"
MAX_ERRORES_SEGUIDOS = 5    # Si falla la lectura tantas veces seguidas, se aborta

# ==========================================
# INICIALIZACIÓN Y CAPTURA
# ==========================================
sdr = None

try:
    sdr = RtlSdr()

    # 1. Desactivar el AGC digital del chip RTL2832U
    sdr.set_agc_mode(False)

    # 2. Fijar la ganancia manual del sintonizador R828D
    #    (esto ya activa el modo manual internamente, pero lo dejamos explícito)
    sdr.set_manual_gain_enabled(True)

    sdr.sample_rate = SAMPLE_RATE
    sdr.center_freq = FRECUENCIA_HZ
    sdr.gain = GAIN_DB

    print("\n--- Conectado con éxito al RTL-SDR Blog V4 ---")
    print(f"Frecuencia central : {sdr.center_freq / 1e6:.3f} MHz")
    print(f"Ganancia fija      : {sdr.gain} dB")
    print(f"Guardando datos en : {NOMBRE_ARCHIVO}\n")

    duracion_total_sec = DURACION_HORAS * 3600
    inicio = time.time()
    errores_seguidos = 0

    with open(NOMBRE_ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "power_dB"])
        f.flush()

        while time.time() - inicio < duracion_total_sec:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            try:
                muestras = sdr.read_samples(256 * 1024)
                potencia_lin = np.mean(np.abs(muestras) ** 2)

                # Evita log10(0) = -inf en el caso límite de potencia nula
                if potencia_lin <= 0:
                    print(f"[{timestamp}] [!] Potencia lineal no válida ({potencia_lin}), se omite muestra.")
                    errores_seguidos += 1
                    time.sleep(INTERVALO_SEC)
                    continue

                potencia_db = 10 * np.log10(potencia_lin)
                writer.writerow([timestamp, f"{potencia_db:.3f}"])
                f.flush()
                print(f"[{timestamp}] Potencia de ruido: {potencia_db:.2f} dB")
                errores_seguidos = 0

            except Exception as e:
                errores_seguidos += 1
                print(f"[{timestamp}] [!] Error de lectura ({errores_seguidos}/{MAX_ERRORES_SEGUIDOS}): {e}")
                if errores_seguidos >= MAX_ERRORES_SEGUIDOS:
                    print("[!] Demasiados errores seguidos, abortando la medición.")
                    break

            time.sleep(INTERVALO_SEC)

except KeyboardInterrupt:
    print("\n[!] Medición detenida por el usuario.")

except Exception as e:
    print(f"\n[!] Error al inicializar o configurar el SDR: {e}")

finally:
    if sdr is not None:
        sdr.close()
        print("[+] Dispositivo SDR liberado correctamente.")

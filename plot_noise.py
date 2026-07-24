import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. Cargar los datos del CSV
NOMBRE_ARCHIVO = "eclipse_ruido_29MHz.csv"  # Asegúrate de coincidir con el CSV generado
df = pd.read_csv(NOMBRE_ARCHIVO)

# 2. Convertir la columna timestamp a formato Datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 3. Configurar la figura
plt.figure(figsize=(12, 6))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# 4. Dibujar la curva de potencia
plt.plot(df['timestamp'], df['power_dB'], color='#e67e22', linewidth=1.2, label='Suelo  de ruido (29 MHz)')

# 5. Formato de títulos y ejes
plt.title("Evolución del suelo de Ruido Solar/Ionosférico en 29.0 MHz", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Hora Local (CEST)", fontsize=11, labelpad=10)
plt.ylabel("Potencia de Ruido Relativa (dB)", fontsize=11)

# 6. Formatear las horas en el eje X para que no se amontonen
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=30, ha='right')

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right')
plt.tight_layout()

# 7. Mostrar la gráfica y guardarla como imagen PNG
plt.savefig("grafica_eclipse_29MHz.png", dpi=300)
print("¡Gráfica guardada exitosamente como 'grafica_eclipse_29MHz.png'!")
plt.show()

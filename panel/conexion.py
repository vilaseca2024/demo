import time
import speedtest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Función para medir la velocidad de Internet
def get_internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convertir a Mbps
    return download_speed

# Configuración inicial de la gráfica
x_vals = np.arange(0, 100, 1)  # Eje X (tiempo)
y_vals = np.zeros_like(x_vals)  # Eje Y (velocidades de descarga)

# Crear la figura y el gráfico
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 100)  # Límites del eje X
ax.set_ylim(0, 100)  # Límites del eje Y (en Mbps)
line, = ax.plot(x_vals, y_vals, label='Velocidad de descarga (Mbps)', color='red')

# Título y etiquetas
ax.set_title("Monitoreo en Tiempo Real de la Velocidad de Internet", fontsize=14)
ax.set_xlabel("Tiempo (s)", fontsize=12)
ax.set_ylabel("Velocidad de descarga (Mbps)", fontsize=12)
ax.legend(loc="upper right")

# Función que actualiza la gráfica
def update(frame):
    # Obtener la nueva velocidad
    new_speed = get_internet_speed()
    
    # Desplazar los valores a la izquierda y agregar el nuevo valor
    y_vals[:-1] = y_vals[1:]
    y_vals[-1] = new_speed
    
    # Actualizar la línea en el gráfico
    line.set_ydata(y_vals)
    
    # Retornar la línea para la animación
    return line,

# Crear la animación en tiempo real
ani = FuncAnimation(fig, update, frames=100, interval=1000, blit=True)

# Mostrar la gráfica
plt.show()

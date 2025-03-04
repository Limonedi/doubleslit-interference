import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

def calculate_intensity(s_width, w_length, s_distance, d_slits, x_vals):
    """Calcula la intensidad de la interferencia de la doble rendija."""
    k = np.pi / (w_length * s_distance)
    
    # Evitar divisiones por cero (cuando x_vals = 0)
    beta = k * s_width * x_vals
    beta[beta == 0] = 1e-10  # Pequeño valor para evitar error numérico
    
    intensity = (np.sin(beta) / beta) ** 2  # Difracción de una sola rendija
    intensity *= np.cos(k * d_slits * x_vals) ** 2  # Interferencia de dos rendijas
    
    return intensity

# Rango de posiciones en la pantalla (de -5 mm a 5 mm)
x_vals = np.linspace(-0.005, 0.005, 1000)

# Parámetros iniciales
slit_width = 100e-6  # 100 µm
wavelength = 500e-9  # 500 nm
screen_distance = 50e-2  # 50 cm
distance_between_slits = 1e-3  # 1 mm

# Cálculo inicial de la intensidad
y_vals = calculate_intensity(slit_width, wavelength, screen_distance, distance_between_slits, x_vals)

# Crear figura y eje
fig, ax = plt.subplots(figsize=(8, 5))
plt.subplots_adjust(bottom=0.25)  # Deja espacio para los sliders

plot, = ax.plot(x_vals * 1e3, y_vals, color='blue', linewidth=1.5)  # Convertimos x a mm
ax.set_xlabel("Distancia desde el centro (mm)")
ax.set_ylabel("Intensidad relativa")
ax.set_title("Simulación de Interferencia en la Doble Rendija")

# Crear sliders en una mejor ubicación
slider_positions = {
    'wavelength': [0.2, 0.05, 0.65, 0.03],
    'slit_width': [0.2, 0.01, 0.65, 0.03],
    'screen_distance': [0.2, 0.09, 0.65, 0.03],
    'distance_between_slits': [0.2, 0.13, 0.65, 0.03]
}

wavelength_slider = Slider(plt.axes(slider_positions['wavelength']), 'Long. Onda (nm)', 100, 1000, valinit=wavelength * 1e9)
slit_width_slider = Slider(plt.axes(slider_positions['slit_width']), "Ancho Rendija (µm)", 10, 1000, valinit=slit_width * 1e6)
screen_distance_slider = Slider(plt.axes(slider_positions['screen_distance']), "Dist. Pantalla (cm)", 10, 100, valinit=screen_distance * 1e2)
distance_between_slits_slider = Slider(plt.axes(slider_positions['distance_between_slits']), "Dist. entre Rendijas (mm)", 0.1, 10, valinit=distance_between_slits * 1e3)

def update(val):
    """Función para actualizar la gráfica cuando los sliders cambian."""
    wavelength = wavelength_slider.val * 1e-9
    slit_width = slit_width_slider.val * 1e-6
    screen_distance = screen_distance_slider.val * 1e-2
    distance_between_slits = distance_between_slits_slider.val * 1e-3
    
    # Recalcular la intensidad
    y_vals = calculate_intensity(slit_width, wavelength, screen_distance, distance_between_slits, x_vals)
    plot.set_ydata(y_vals)
    fig.canvas.draw_idle()

# Conectar los sliders con la función update
wavelength_slider.on_changed(update)
slit_width_slider.on_changed(update)
screen_distance_slider.on_changed(update)
distance_between_slits_slider.on_changed(update)

plt.show()

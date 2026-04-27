"""5. Calcular las pérdidas de calor a través de la unidad de superficie del revestimiento de ladrillo de una
caldera de vapor en la zona de instalación del economizador de agua de alimentación y las temperaturas
en las superficies de la pared si el espesor de ésta es e=250 mm , la temperatura de los gases es t1 =
700ºC y la temperatura del aire en la sala de calderas es de t2 = 30ºC. El coeficiente de traspaso del calor
de los gases a la superficie de la pared es α1=19.8 kcal/m2 .h.ºC; y de la pared al aire es α 2 =12 W/m2.ºC.
El coeficiente de conductividad térmica de la pared es k = 0.7 W/m.ºC. """



# Conducción
#Electrones libres: Son los electrones libres los que transportan la energía térmica de un punto a otro en el sólido(mejores cond.: metales puros)
#Moléculas en niveles energéticos mayores ceden energía a moléculas adyacentes
# Ley de  Fourier:
# q / A = -k * dT / dx
# k: conductancia térmica del material, que depende de la naturaleza del material y de su temperatura. Se mide en W/(m.ºC) o kcal/(m.h.ºC).

# Convección 
# Modo de transferencia de energía térmica entre una superficie sólida o interfase y el fluido adyacente (líquido o gas). Comprende los efectos combinados de la conducción y el movimiento del fluido. Existe movimiento macroscópico de las partículas del fluido. En ausencia de dicho movimiento el calor se transfiere por conducción pura.
# Ley de enfriamiento de Newton:
# q = α * A * (t1 - t2)
# arfha: coeficiente de transferencia de calor por convección.


# Datos del problema:
# Rebestimiento de ladrillo de una caldera de vapor
e = 0.25  # m

# Temperaturas:
t1 = 700   # °C (temperatura de los gases)
t2 = 30    # °C (temperatura del aire en la sala de calderas)
# No sabemos la temperatura en la superficie de las paredes, tc1 y tc2.
alfha1 = 19.8 * 1.163  # kcal/(m².h.ºC) a W/(m².ºC)
alfha2 = 12  # W/(m².ºC)
k = 0.7      # W/(m.ºC) 


# --- Calculo de las perdida de calor ---
# Es problema se puede entender como la conecion de tres resistencias térmicas en serie: la resistencia de convección de los gases, la resistencia de conducción a través del ladrillo, y la resistencia de convección hacia el aire ambiente.

q = (t1 - t2) / (1 / alfha1 + e / k + 1 / alfha2)

print(f"Flujo de calor q: {q:.2f} W/m²")


# --- Calculo de las temperaturas en las superficies de la pared ---
# Formula de conveccion de los gases:
# q = alfha1 * (t1 - tc1)
ts1 = t1 - q / alfha1

# Formula de conveccion hacia el aire ambiente:
# q = alfha2 * (tc2 - t2)
ts2 = t2 + q / alfha2

print(f"Temperatura pared interna de las gases ts1: {ts1:.2f} °C")
print(f"Temperatura pared externa hacia el aire ts2: {ts2:.2f} °C")




""" 1. El Escenario: El EconomizadorUna caldera no es solo un tanque con fuego. Los gases calientes que
 salen de la combustión todavía tienen mucha energía. El economizador es un intercambiador de calor 
 ubicado en el conducto de escape (la chimenea o "fuego muerto"). Su función es usar esos gases para 
 precalentar el agua antes de que entre a la caldera.
 
 2. La "Pared" que estamos analizandoEstamos parados justo en el muro lateral que envuelve ese sector. 
 Imagina que es una pared de ladrillo de 25 cm de espesor.
 -A un lado (Adentro): Pasan los gases de combustión que están a 700°C. Estos gases no tocan 
 directamente el aire de afuera; primero deben "golpear" la pared de ladrillo. Esa transferencia del 
 gas al ladrillo es la convección interna ($\alpha_1$).
 -En el medio (La pared): El calor viaja a través del ladrillo rojo de 250 mm. Esto es conducción ($k$).
-Al otro lado (Afuera): Estamos en la "sala de calderas" (donde caminan los operarios). El aire ahí 
está a 30°C. El calor que logró cruzar el ladrillo ahora sale al aire de la sala. Esa transferencia de 
la pared al aire es la convección externa ($\alpha_2$). """


""" import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualizar_caldera_3d():
    # --- Datos del problema (Calculados previamente) ---
    e = 0.25      # Espesor pared (m)
    t1 = 700      # Gases (°C)
    ts1 = 639.87  # Cara interna (°C)
    ts2 = 145.41  # Cara externa (°C)
    t2 = 30       # Aire sala (°C)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # --- 1. Dibujar la Pared de Ladrillo ---
    # Definimos los vértices de la pared (X=espesor, Y=ancho, Z=alto)
    # La pared va desde x=0 hasta x=e
    v = np.array([[0, 0, 0], [e, 0, 0], [e, 1, 0], [0, 1, 0],
                  [0, 0, 1], [e, 0, 1], [e, 1, 1], [0, 1, 1]])
    
    # Caras de la pared
    faces = [
        [v[0], v[1], v[5], v[4]], # Abajo
        [v[1], v[2], v[6], v[5]], # Cara externa (ts2)
        [v[2], v[3], v[7], v[6]], # Arriba
        [v[3], v[0], v[4], v[7]], # Cara interna (ts1)
        [v[0], v[1], v[2], v[3]], # Fondo
        [v[4], v[5], v[6], v[7]]  # Techo
    ]

    # Color de la pared (gradiente de rojo/naranja según temperatura)
    poly = Poly3DCollection(faces, alpha=0.7, edgecolor='black')
    poly.set_facecolor(['peru', 'orange', 'peru', 'red', 'peru', 'peru'])
    ax.add_collection3d(poly)

    # --- 2. Simulación de Gases (Interno: x < 0) ---
    # Gases subiendo (Z de 0 a 1)
    z_gases = np.linspace(0, 1, 15)
    y_gases = np.linspace(0.1, 0.9, 5)
    ZG, YG = np.meshgrid(z_gases, y_gases)
    XG = np.zeros_like(ZG) - 0.2 # Posición a la izquierda de la pared
    
    # Flechas de gases (Rojas, largas = alta velocidad/temp)
    ax.quiver(XG, YG, ZG, 0, 0, 0.15, color='red', length=0.8, normalize=True, label=f'Gases (T1={t1}°C)')

    # --- 3. Simulación de Aire (Externo: x > e) ---
    # Aire ambiente con movimiento errático o lento
    z_aire = np.linspace(0.1, 0.9, 8)
    y_aire = np.linspace(0.1, 0.9, 4)
    ZA, YA = np.meshgrid(z_aire, y_aire)
    XA = np.zeros_like(ZA) + e + 0.2
    
    # Flechas de aire (Azules, cortas = baja velocidad)
    ax.quiver(XA, YA, ZA, 0, 0, 0.05, color='blue', length=0.4, normalize=True, label=f'Aire Sala (T2={t2}°C)')

    # --- 4. Etiquetas de Temperatura ---
    # Etiqueta t_s1
    ax.text(0, 0.5, 1.1, f"ts1: {ts1}°C", color='darkred', fontweight='bold')
    # Etiqueta t_s2
    ax.text(e, 0.5, 1.1, f"ts2: {ts2}°C", color='darkblue', fontweight='bold')
    
    # --- Configuración de la vista ---
    ax.set_xlim(-0.5, e + 0.5)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1.2)
    ax.set_xlabel('Espesor (m)')
    ax.set_ylabel('Ancho Pared')
    ax.set_zlabel('Altura (Flujo)')
    ax.set_title('Esquema 3D: Transferencia de Calor en Caldera (Economizador)')
    ax.legend(loc='upper left')

    # Ajustar ángulo de visión
    ax.view_init(elev=20, azim=-45)

    plt.show()

if __name__ == "__main__":
    visualizar_caldera_3d() """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def simular_fluidos_caldera():
    
    num_particulas = 40  # Cantidad por lado

    # --- Configuración de la Escena ---
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    # Cambiar la distancia de la cámara (Zoom)
    # Valores menores a 10 acercan la cámara, mayores la alejan.
    ax.set_box_aspect(None, zoom=1.2) # En versiones modernas de Matplotlib

    # O para versiones anteriores:
    ax.dist = 8  # Por defecto es 10. Menos es más cerca.

    # Cambiar el ángulo de visión inicial
    ax.view_init(elev=10, azim=-80, roll=0) # Elevación y Azimut

    # --- Inicialización de Partículas ---
    # Gases (Izquierda: x < 0)
    pos_gases = np.zeros((num_particulas, 3))
    pos_gases[:, 0] = np.random.uniform(-0.4, -0.1, num_particulas) # X
    pos_gases[:, 1] = np.random.uniform(0, 1, num_particulas)      # Y
    pos_gases[:, 2] = np.random.uniform(0, 1, num_particulas)      # Z

    # Aire (Derecha: x > e)
    pos_aire = np.zeros((num_particulas, 3))
    pos_aire[:, 0] = np.random.uniform(e + 0.1, e + 0.4, num_particulas)
    pos_aire[:, 1] = np.random.uniform(0, 1, num_particulas)
    pos_aire[:, 2] = np.random.uniform(0, 1, num_particulas)

    # Creamos los objetos gráficos (bolitas)
    scat_gases = ax.scatter(pos_gases[:, 0], pos_gases[:, 1], pos_gases[:, 2], 
                            color='red', s=30, label=f'Gases ({t1}°C)')
    scat_aire = ax.scatter(pos_aire[:, 0], pos_aire[:, 1], pos_aire[:, 2], 
                           color='cyan', s=20, alpha=0.6, label=f'Aire ({t2}°C)')

    # --- Dibujo de la Pared (Cubo estático) ---
    def dibujar_pared():
        # Ladrillo interno (caliente)
        x_p = [0, e, e, 0, 0]
        y_p = [0, 0, 1, 1, 0]
        for z in [0, 1]:
            ax.plot(x_p, y_p, [z]*5, color='brown', lw=2)
        for i in range(4):
            ax.plot([x_p[i], x_p[i]], [y_p[i], y_p[i]], [0, 1], color='brown', lw=2)

        # --- 1. Dibujar la Pared de Ladrillo ---
    # Definimos los vértices de la pared (X=espesor, Y=ancho, Z=alto)
    # La pared va desde x=0 hasta x=e
    v = np.array([[0, 0, 0], [e, 0, 0], [e, 1, 0], [0, 1, 0],
                  [0, 0, 1], [e, 0, 1], [e, 1, 1], [0, 1, 1]])
    
    # Caras de la pared
    faces = [
        [v[0], v[1], v[5], v[4]], # Abajo
        [v[1], v[2], v[6], v[5]], # Cara externa (ts2)
        [v[2], v[3], v[7], v[6]], # Arriba
        [v[3], v[0], v[4], v[7]], # Cara interna (ts1)
        [v[0], v[1], v[2], v[3]], # Fondo
        [v[4], v[5], v[6], v[7]]  # Techo
    ]
    

    # Color de la pared (gradiente de rojo/naranja según temperatura)
    poly = Poly3DCollection(faces, alpha=0.7, edgecolor='black')
    poly.set_facecolor(['peru', 'orange', 'peru', 'red', 'peru', 'peru'])
    ax.add_collection3d(poly)
        
    # Etiquetas de temperatura en la superficie
    ax.text(-0.1, 0.5, 1.2, f"ts1: {ts1:.2f}°C", color='red', fontsize=10, fontweight='bold')
    ax.text(e + 0.1, 0.5, 1.2, f"ts2: {ts2:.2f}°C", color='blue', fontsize=10, fontweight='bold')
    ax.text(-0.6, 0.5, 1.1, f"t1: {t1:.2f}°C", color='red', fontsize=10, fontweight='bold')
    ax.text(e + 0.4, 0.5, 1.1, f"t2: {t2:.2f}°C", color='purple', fontsize=10, fontweight='bold')

    # --- Función de Actualización (Animación) ---
    def update(frame):
        # 1. Mover Gases (Rápido hacia arriba en Z)
        pos_gases[:, 2] += 0.03  # Velocidad
        # Resetear si salen de la caja
        indices_fuera = pos_gases[:, 2] > 1.1
        pos_gases[indices_fuera, 2] = -0.1
        
        # 2. Mover Aire (Lento y un poco aleatorio)
        pos_aire[:, 2] += 0.005  # Velocidad mucho menor
        pos_aire[:, 1] += np.random.normal(0, 0.002, num_particulas) # Vibración
        indices_fuera_aire = pos_aire[:, 2] > 1.1
        pos_aire[indices_fuera_aire, 2] = -0.1

        # Actualizar posiciones en el gráfico
        scat_gases._offsets3d = (pos_gases[:, 0], pos_gases[:, 1], pos_gases[:, 2])
        scat_aire._offsets3d = (pos_aire[:, 0], pos_aire[:, 1], pos_aire[:, 2])
        
        return scat_gases, scat_aire

    # Configuración de límites y etiquetas
    ax.set_xlim(-0.6, e + 0.6)
    ax.set_ylim(-0.1, 1.1)
    ax.set_zlim(-0.1, 1.2)
    ax.set_xlabel('Espesor (m)')
    ax.set_title('Simulación de Flujo de Partículas: Pared de Caldera')
    ax.legend(loc='upper left')
    
    dibujar_pared()
    
    # Crear animación
    ani = FuncAnimation(fig, update, frames=200, interval=30, blit=False)
    
    plt.show()

if __name__ == "__main__":
    simular_fluidos_caldera()
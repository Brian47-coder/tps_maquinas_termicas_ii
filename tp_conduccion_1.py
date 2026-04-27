"""1.Una pared plana está construida con ladrillo refractario con un espesor e = 250 mm ,las temperaturas de
sus caras laterales son : t1 = 1350 ºC y t2 = 50 ºC. El coeficiente de conductividad térmica del ladrillo
refractario es función de la temperatura , k= 0.838.(1+0.0007.t )W/m.ºC . Calcular y representar a escala
la distribución de las temperaturas en la pared."""

import numpy as np
import matplotlib.pyplot as plt


e = 0.25  # Espesor en metros
t1 = 1350  # Temperatura en la cara 1 en ºC
t2 = 50    # Temperatura en la cara 2 en ºC
k0 = 0.838 # Conductividad térmica a temperatura de referencia en W/m.ºC
beta = 0.0007 # Coeficiente de variación de la conductividad térmica.


# Ecuación de conducción de calor en estado estacionario:
# Ley de Fourier: Q = -k * A * (dT/dx) --->  q = -k * (dT/dx)   
# A es constante en pared plana

# Para resolver la distribución de temperatura, se puede usar la ecuación diferencial:
# q * dx = -[0.838.(1+0.0007.t )] * dT
# Integrando esta ecuación desde t1 a t2 y desde 0 a e, se obtiene la distribución de temperatura T(x).

# q * e = -0.838 * (T2 - T1) -0.838 * 0.0007 * (T2² - T1²) / 2

# q = [-0.838 * (T2 - T1) -0.838 * 0.0007 * (T2² - T1²) / 2] / e

q = (-0.838 * (t2 - t1) - 0.838 * 0.0007 * (t2**2 - t1**2) / 2) / e

# Otro forma de calcular
k_prom = k0 * (1 + beta * (t1 + t2) / 2) 

q_prom = -k_prom * (t2 - t1) / e

print(f"Flujo de calor q: {q:.2f} W/m²")
print(f"Flujo de calor q_prom: {q_prom:.2f} W/m²")


""" Cuando la conductividad térmica k depende linealmente de la temperatura, 
la distribución de temperatura T(x) es parabólica, no lineal."""
#q * x = k_0 * [ (t_1 - T) + (beta / 2) * (t_1^2 - T^2)]
# (q * x) / k_0 =  (t_1 - T) + (beta / 2) * (t_1^2 - T^2)
# -(t_1 - T) - (beta / 2) * (t_1^2 - T^2) + (q * x) / k_0 = 0 
# -t_1 + T - (beta / 2)*t_1^2 + (beta / 2)*T^2 + (q * x) / k_0 = 0
# +(beta / 2)*T^2 + T + [(q * x) / k_0 - t_1 -(beta / 2)*t_1^2]= 0 

# Distribución No Lineal de Temperatura T(x)
# Despejando T de la ecuación cuadrática: (beta/2)T² + T - [(beta/2)t1² + t1 - (q*x/k0)] = 0

# Discretización del espesor de la pared
x = np.linspace(0, e, 50)  # 50 puntos entre 0 y e
# Inicialización del arreglo de temperaturas
T_lista = []

for xi in x:
    # Coeficientes de la ecuación cuadrática
    a = beta / 2
    b = 1
    c =(-(beta / 2) * t1**2 - t1 + (q * xi / k0))

    # Aplicamos la resolvente
    discriminante = b**2 - 4*a*c

    T_sol = (-b + np.sqrt(discriminante)) / (2*a)  # Tomamos la solución positiva
    T_lista.append(T_sol)

T_lineal = np.linspace(t1, t2, 50)  # Distribución lineal de temperatura para comparación

 
# Grafico de la distribucion de temperatura en el esperos de la pared
plt.plot(x, T_lista, 'r-', linewidth=2, label='Distribución real (k variable)')

#Grafico distribusion lineal de la temperatura
plt.plot(x, T_lineal, 'y--', linewidth=1.5, label='Distribución lineal (k constante)')

# Puntos para temperaturas de los extremos
plt.plot(0, t1, 'bo', markersize=10, label=f'Temperatura t1 = {t1} °C')  # Punto azul en x=0, y=t1
plt.plot(e, t2, 'go', markersize=10, label=f'Temperatura t2 = {t2} °C')  # Punto verde en x=e, y=t2

plt.plot([0, 0], [t1*2, 0], 'black')
plt.plot([e, e], [t1*2, 0], 'black')
plt.plot([0, e], [t1*2, t1*2], 'black')
plt.plot([0, e], [0, 0], 'black')



plt.title('Distribución de Temperatura en la Pared')
plt.xlabel('Espesor (m)')
plt.ylabel('Tempratura (°C)')
plt.legend()
plt.grid()
plt.show()



  






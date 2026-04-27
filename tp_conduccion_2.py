"""2.La pared plana de un tanque son de área F= 5 m2 ,está cubierta con aislante térmico de dos capas. La
pared del tanque es de acero con espesor e1 =8 mm y coeficiente de conductividad térmica k1 =46.5
W/m.ºC . La primera capa de aislante es de un material de conductividad térmica k2 = 0.144 + 0.00014.t
W/m.ºC y espesor e2=50 mm. La segunda capa de aislante, con espesor e3= 10 mm, es un enlucido
(revoque) de mortero de cal cuyo coeficiente de conductividad térmica es k3 = 0.693 W/mºC . La
temperatura de la superficie interna de la pared del tanque es t1 = 5ºC y la superficie exterior del aislante
está a la temperatura t4=20ºC . Calcular la cantidad de calor que se recibe a través de la pared, las
temperaturas entre capas, construir gráfico de distribución de las temperaturas. """
import numpy as np
import matplotlib.pyplot as plt     # plt es una clase o funcion? : Es un módulo de Matplotlib que se utiliza para crear gráficos y visualizaciones en Python. Proporciona una interfaz para generar gráficos de manera sencilla y personalizable. En este código, se utiliza para graficar la distribución de temperaturas a través de las capas de la pared del tanque.
from scipy.optimize import fsolve   # fsolve es una función de scipy para resolver sistemas de ecuaciones no lineales. Se usará para encontrar t2 y t3.

# Datos del problema
# En total son 3 espesores, para calcular la conduccion.
A = 5    # m²

# Acero:
e1 = 0.008 # m
k1 = 46.5  # W/(m.°C)

# Capa de aislante 1:
e2 = 0.050 # m
# k2 es función de la temperatura, se calculará posteriormente
# k2 = 0.144 + 0.00014.t
k02 = 0.144
beta_2 = 0.00014 / k02
k2 = lambda t: k02 * (1 + beta_2 * t)

# Capa de aislante 2: mortero de cal
e3 = 0.010 # m
k3 = 0.693 # W/(m.°C) 

# Temperaturas:
t1 = 5    # °C (superficie interna de la pared del tanque)
t4 = 20   # °C (superficie exterior del aislante)


# Análisis del Problema
# El flujo de calor Q es constante a través de las tres capas:


# Definimos el sistema de ecuaciones para hallar t2 y t3
def ecuaciones(vars):
    t2, t3 = vars
    k2_prom = 0.144 + 0.00014 * (t2 + t3) / 2
    
    # El flujo Q debe ser igual en las 3 capas (Q/A = q)
    q1 = k1 * (t2 - t1) / e1
    q2 = k2_prom * (t3 - t2) / e2
    q3 = k3 * (t4 - t3) / e3
    
    return [q1 - q2, q2 - q3]

def ecuaciones_1(vars):
    t2, t3 = vars
    
    # El flujo Q debe ser igual en las 3 capas (Q/A = q)
    q1 = k1 * (t2 - t1) / e1
    q2 = (k02 * (t3 - t2) + k02 * beta_2 * (t3**2 - t2**2) / 2) / e2
    q3 = k3 * (t4 - t3) / e3
    
    return [q1 - q2, q2 - q3]

# Resolvemos (estimación inicial t2=10, t3=15) y obtenemos t2 y t3 que cumplen el equilibrio de flujos:
t2, t3 = fsolve(ecuaciones, [10, 15])
t22, t33 = fsolve(ecuaciones_1, [6, 10])

# Calculamos el calor Q usando cualquiera de las capas (usamos la capa 1):
Q = (k1 * A / e1) * (t2 - t1)

# Calculamos el valor promedio de k2 para la capa 2:
k2_prom = 0.144 + 0.00014 * (t2 + t3) / 2

print(f"Temperaturas de interfaz: t1 = {t1:.2f}°C, t2 = {t2:.2f}°C, t3 = {t3:.2f}°C, t4 = {t4:.2f}°C" )
print(f"Temperaturas de interfaz: t1 = {t1:.2f}°C, t2 = {t22:.2f}°C, t3 = {t33:.2f}°C, t4 = {t4:.2f}°C" )


print(f"Calor capa 1: Q1 = {k1 * A * (t2 - t1) / e1:.2f} W")
print(f"Calor capa 2: Q2 = {k2_prom * A * (t3 - t2) / e2:.2f} W")
print(f"Calor capa 3: Q2_exacto = {A * (k02 * (t3 - t2) + k02 * beta_2 * (t3**2 - t2**2) / 2) / e2:.2f} W")
print(f"Calor capa 3: Q3 = {k3 * A *(t4 - t3) / e3:.2f} W")

print(f"Calor total Q: {Q:.2f} W")
print(f"Flujo de calor q: {Q/A:.2f} W/m²")

# --- CONSTRUCCIÓN DEL GRÁFICO ---
# Capa 1: Lineal (acero)
x1 = np.linspace(0, e1, 10)
T1 = np.linspace(t1, t2, 10) 

# Capa 2: No lineal (Parabólica)
x2 = np.linspace(e1, e1 + e2, 50)
dist_x2 = x2 - e1  # esto se hace para que el origen de la capa 2 sea 0, facilitando el cálculo de T2(x), pero se grafica desde x2.

k0_2 = 0.144
beta_2 = 0.00014 / k0_2

q = Q / A

T2 = []
for xi in dist_x2:
    a = beta_2 / 2
    b = 1
    c = -((beta_2/2)*t2**2 + t2 + (q * xi / k0_2))
    determinante = b**2 - 4*a*c
    # Usamos la resolvente para el perfil parabólico
    temp = (-b + np.sqrt(determinante)) / (2*a)
    T2.append(temp)

# Capa 3: Lineal (mortero)
x3 = np.linspace(e1 + e2, e1 + e2 + e3, 10)
T3 = np.linspace(t3, t4, 10) # Lineal en mortero

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x1, T1, 'b-', label='Acero (k cte)')
plt.plot(x2, T2, 'r-', label='Aislante (k variable)')
plt.plot(x3, T3, 'g-', label='Mortero (k cte)')

# Puntos para temperaturas de los extremos
plt.plot(0, t1, 'bo', markersize=10, label=f'Temperatura t1 = {t1} °C')  # Punto azul en x=0, y=t1
plt.plot(e1, t2, 'ro', markersize=10, label=f'Temperatura t2 = {t2:.2f} °C')  # Punto rojo en x= e1, y=t2
plt.plot(e1 + e2, t3, 'go', markersize=10, label=f'Temperatura t3 = {t3:.2f} °C')  # Punto verde en x= e1+e2, y=t3
plt.plot(e1 + e2 + e3, t4, 'mo', markersize=10, label=f'Temperatura t4 = {t4:.2f} °C')  # Punto morado en x= e1+e2+e3, y=t4


# Decoración
plt.axvline(0, color='gray', linestyle='--')
plt.axvline(e1, color='gray', linestyle='--')
plt.axvline(e1+e2, color='gray', linestyle='--')
plt.axvline(e1+e2+e3, color='gray', linestyle='--')
plt.title("Distribución de Temperaturas en Pared Compuesta")
plt.xlabel("Espesor acumulado [m]")
plt.ylabel("Temperatura [°C]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()



# Creamos una línea recta teórica para comparar
T2_lineal = np.linspace(t2, t3, 50)

plt.figure(figsize=(10, 6))

# Graficamos la curva real (parabólica)
plt.plot(x2, T2, 'r-', linewidth=3, label='Distribución Real (Parabólica)')

# Graficamos una línea punteada que une t2 y t3 para ver la diferencia
plt.plot(x2, T2_lineal, 'k--', alpha=0.6, label='Referencia Lineal (k = cte)')

# --- ZOOM EN LA CAPA 2 ---
# Ajustamos los límites para ver solo la zona donde k varía
plt.xlim(e1 - 0.005, e1 + e2 + 0.005)
plt.ylim(t2 - 1, t3 + 1)


plt.title("Efecto de la Conductividad Variable en la Capa 2 (Zoom)")
plt.legend()
plt.grid(True, which='both', linestyle=':', alpha=0.5) # with='both' para mostrar cuadrícula mayor y menor
plt.show()


# Para demostrarlo numéricamente:
diferencias = np.abs(np.array(T2) - T2_lineal)   # np.array es un 
desviacion_maxima = np.max(diferencias)
print(f"Desviación máxima de la parábola respecto a la recta: {desviacion_maxima:.5f} °C")

"""Conclusion: En este caso, t1 = 5°C (interior) y t4 = 20°C (exterior), por lo que el calor 
fluye del exterior al interior (el tanque está en un ambiente más cálido). Esto es posible en 
escenarios como un tanque refrigerado en un día caluroso. El cálculo es el mismo, pero el 
flujo q es positivo hacia el interior. Si fuera t1 > t4, el flujo sería negativo.

La función es:

k(T)=k0 * (1+βT)
Es lineal en T

Entonces pasa algo MUY importante:

Cuando 
k(T) es lineal: El promedio de la función ≈ valor en el punto medio

"""
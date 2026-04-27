""" 4. Se ha decidido disminuir dos veces el espesor de la capa de ladrillo rojo del revestimiento del hogar
examinado en el problema anterior y poner entre las capas un relleno de migajas de diatomita cuyo
coeficiente de conductividad térmica es k= 0.113+0.00023.t W/m.ºC . Cuál debe ser el espesor del
relleno de diatomita para que las pérdidas de calor permanezcan invariables cuando las temperaturas en
las superficies exteriores de la pared sean las mismas que en el problema anterior. """



import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from tp_3 import ecuacion_de_calor



# Datos del problema:
# Magnesita alveolada
e1 = 0.125  # m
k01 = 0.28  # W/(m.ºC) 
beta_1 = 0.00023 / k01
k1 = lambda t: k01 * (1 + beta_1 * t)  # W/m.ºC 

# Relleno de migajas de diatomita
# Se debe calcular el espesor ec
k0c = 0.113
beta_c = 0.00023 / k0c
kc = lambda t: k0c * (1 + beta_c * t)  # W/(m.°C)

# Ladrillo rojo
e2 = 0.500 / 2 # m   # Mitad del espesor se utiliza
k2 = 0.7    # W/(m.ºC)


# Por lo que la temperatura en la superficie de contacto se deben calcular tc1  tc2.
#Temperaturas:
t1 = 1100   # °C (superficie interior del hogar)
t2 = 50     # °C (superficie exterior del hogar)


# Perdidas 
q = ecuacion_de_calor()
print(f"calor q: {q:.2f} W/m²")



# ---- Calculamos la temperatura de contacto tc1 y tc2 con el nuevo espesor ec ----
# Capa 1: magnesita alveolada
# despejamos la temperatura tc1 de la ecuacion q1 = (- k01 * (tc1 - t1) - k01 * beta_1 * (tc1**2 - t1**2) / 2) / e1
def ecuacion_tc1(tc1):
    q1 = (- k01 * (tc1 - t1) - k01 * beta_1 * (tc1**2 - t1**2) / 2) / e1
    return q1 - q

tc1_sol = fsolve(ecuacion_tc1, 510)[0] # Valor inicial para la solución
print(f"Temperatura de contacto tc1: {tc1_sol:.2f} °C")

# Capa 3: ladrillo rojo
# Despejamos la temperatura tc2 de la ecuacion q3 = -k2 * (t2 - tc2) / e2
#q = -k2 * t2 / e2 + k2 * tc2 / e2
tc2 = (q + k2 * t2 / e2) * e2 / k2
#print(f"Temperatura de contacto tc2: {tc2:.2f} °C")

def ecuacion_tc2(tc2):
    q3 = -k2 * (t2 - tc2) / e2
    return q3 - q

tc2_sol = fsolve(ecuacion_tc2, 300)[0] # Valor inicial para la solución
print(f"Temperatura de contacto tc2: {tc2_sol:.2f} °C")


# Despejamos de la ecuacion el espesor ec, q2 = (- k0c * (tc2 - tc1) - k0c * beta_c * (tc2**2 - tc1**2) / 2) / ec
ec = (- k0c * (tc2_sol - tc1_sol) - k0c * beta_c * (tc2_sol**2 - tc1_sol**2) / 2) / q
print(f"Espesor del relleno de diatomita ec: {ec:.4f} m")



q1 = (- k01 * (tc1_sol - t1) - k01 * beta_1 * (tc1_sol**2 - t1**2) / 2) / e1
q2 = (- k0c * (tc2_sol - tc1_sol) - k0c * beta_c * (tc2_sol**2 - tc1_sol**2) / 2) / ec
q3 = -k2 * (t2 - tc2_sol) / e2

print(f"Flujo de calor en la capa 1: {q1:.2f} W/m²")
print(f"Flujo de calor en la capa 2: {q2:.2f} W/m²")
print(f"Flujo de calor en la capa 3: {q3:.2f} W/m²")

if np.isclose(q1, q2) and np.isclose(q2, q3):
    print("Los flujos de calor son iguales en todas las capas.")
else:
    print("Los flujos de calor no son iguales. Revisar cálculos.")



# ----- GRÁFICO -----
# Capa 1: variación parabólica de la temperatura
x1 = np.linspace(0, e1, 50)
T1 = []     #inicializamos

for xi in x1:
    # Coeficientes de la ecuación cuadrática
    a = beta_1 / 2
    b = 1
    c =(-(beta_1 / 2) * t1**2 - t1 + (q1 * xi / k01))

    discriminante = b**2 - 4*a*c

    T_sol = (-b + np.sqrt(discriminante)) / (2*a)  # Tomamos la solución positiva
    T1.append(T_sol)

# Varaiacion lineal de la temperatura capa 1
T11 = np.linspace(t1, tc1_sol, 50)


# Capa c: variación parabólica de la temperatura
xc = np.linspace(e1, e1 + ec, 50)
dist_c = xc - e1  # esto se hace para que el origen de la capa c sea 0, facilitando el cálculo de Tc(x), pero se grafica desde xc.
Tc = []     #inicializamos

for xi in dist_c:
    # Coeficientes de la ecuación cuadrática
    a = beta_c / 2
    b = 1
    c =(-(beta_c/ 2) * tc1_sol**2 - tc1_sol + (q1 * xi / k0c))

    discriminante = b**2 - 4*a*c

    Tc_sol = (-b + np.sqrt(discriminante)) / (2*a)  # Tomamos la solución positiva
    Tc.append(Tc_sol)

# Varaiacion lineal de la temperatura capa c
Tcc = np.linspace(tc1_sol, tc2_sol, 50)

# Capa 2: variación lineal de la temperatura
x2 = np.linspace(e1 + ec, e1 + ec + e2, 50)
T2 = np.linspace(tc2_sol, t2, 50)

plt.figure(figsize=(10, 6))
plt.plot(x1, T11, 'black', linewidth=2, linestyle='--')
plt.plot(x1, T1, 'purple', linewidth=2, label='Magnesita (k variable - Parabólico)')

plt.plot(xc, Tcc, 'black', linewidth=2, linestyle='--')
plt.plot(xc, Tc, 'green', linewidth=2, label='Diatomita (k variable - Parabólico)')

plt.plot(x2, T2, 'cyan', linewidth=2, label='Ladrillo Rojo (k constante - Lineal)')

# Detalles visuales
plt.axvline(0, color='black', linestyle='--')
plt.axvline(e1, color='black', linestyle='--')
plt.axvline(e1 + ec, color='black', linestyle='--')
plt.axvline(e1 + ec + e2, color='black', linestyle='--')
plt.text(e1, tc1_sol + tc1_sol*0.1, f' {tc1_sol:.1f}°C', color='black')
plt.text(e1 + ec, tc2_sol + tc2_sol*0.1, f' {tc2_sol:.1f}°C', color='black')

# Puntos para temperaturas de los extremos
plt.plot(0, t1, 'bo', markersize=10, label=f'Temperatura t1 = {t1} °C')  # Punto azul en x=0, y=t1
plt.plot(e1, tc1_sol, 'ro', markersize=10, label=f'Temperatura tc1 = {tc1_sol:.2f} °C')  # Punto rojo en x= e1, y=tc1
plt.plot(e1 + ec, tc2_sol, 'yo', markersize=10, label=f'Temperatura tc2 = {tc2_sol:.2f} °C')  # Punto verde en x= e1+ec, y=tc2
plt.plot(e1 + ec + e2, t2, 'go', markersize=10, label=f'Temperatura t2 = {t2} °C')  # Punto verde en x= e1+ec+e2, y=t2

plt.title("Distribución de Temperatura en la Pared de la Caldera")
plt.xlabel("Espesor [m]")
plt.ylabel("Temperatura [°C]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()






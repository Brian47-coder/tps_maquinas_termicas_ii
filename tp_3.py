"""3.La pared del hogar sin protección de una caldera de vapor está fabricada de magnesita alveolada con
espesor e1 =125 mm y de una capa de ladrillo rojo cuyo espesor es e2 =500 mm . Las capas están bien
ajustadas entre sí (no hay resistencia de contacto). La superficie interior del hogar es t1 =1100ºC y en la
superficie exterior t2 = 50ºC .El coeficiente de conductividad térmica de la magnesita alveolada es k1 =
0.28+0.00023.t W/m.ºC y el del ladrillo rojo es k2 =0.7 W/m.ºC. Calcular las pérdidas de calor en kcal/h a
través de 1 m2 de pared del hogar y la temperatura en la superficie de contacto de las capas. """

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Datos del problema:
# Magnesita alveolada
e1 = 0.125  # m
k01 = 0.28  # W/(m.ºC) 
beta_1 = 0.00023 / k01
k1 = lambda t: k01 * (1 + beta_1 * t)  # W/m.ºC 

# Ladrillo rojo
e2 = 0.500  # m
k2 = 0.7    # W/(m.ºC)

#Entonces k1 no es un número, es una función. Se usa así:
valor = k1(100)  # calcula 0.28 + 0.00023 * 100



# NO hay resistencia de contacto, por lo que la temperatura en la superficie de contacto es la misma para ambas capas.
#Temperaturas:
t1 = 1100   # °C (superficie interior del hogar)
t2 = 50     # °C (superficie exterior del hogar)



# Analisis del problema:
# Tenemmos dos incognitas principales: El flujo de calor q y la temperatura de contacto T_c.


# Capa 1: variacion parabolica de la temperatura
# q * dx = -[k01 * (1 + beta_1 * t )] * dT
# Integrando esta ecuación desde t1 a tc y desde 0 a e, se obtiene la distribución de temperatura T(x).
# q * e1 = - k01 * (tc - t1) - k01 * beta_1 * (tc² - t1²) / 2
# q = [- k01 * (tc - t1) - k01 * beta_1 * (tc² - t1²) / 2] / e1


# Capa 2: variacion lineal 
# q * dx = -k2 * dT
# Integrando esta ecuación desde tc a t2 y desde e1 a e2:
# q = -k2 * (t2 - tc) / e2



# Igualando los flujos de calor q
def ecuacion(tc):
    q1 = (- k01 * (tc - t1) - k01 * beta_1 * (tc**2 - t1**2) / 2) / e1
    q2 = -k2 * (t2 -tc) / e2
    return q1 - q2



if __name__ == "__main__" :
    # Resolvemos (estimación inicial tc = 500) y obtenemos tc que cumplen el equilibrio de flujos:
    tc_array = fsolve(ecuacion, 500)
    tamano = len(tc_array)
    print(f"El array tiene {tamano} elementos")

    # convertimos el resultado a float:
    tc_sol = float(tc_array[0])
    print(f"Temperatura de contacto T_c: {tc_sol:.2f} °C")
    print(type(tc_sol))


    #Calculo del flujo de calor
    q1 = (- k01 * (tc_sol - t1) - k01 * beta_1 * (tc_sol**2 - t1**2) / 2) / e1
    q2 = - k2 * (t2 - tc_sol) / e2
    print(f"Flujo de calor q1: {q1:.2f} W/m²")
    print(f"Flujo de calor q2: {q2:.2f} W/m²")

    # 2. Calcular flujo de calor q (W/m2)
    q_w = k2 * (tc_sol - t2) / e2

    # 3. Conversión a kcal/h (1 W = 0.860421 kcal/h)
    q_kcal = q_w * 0.860421
    print(f"Flujo de calor q_w: {q_w:.2f} W/m²")
    print(f"Flujo de calor q_kcal: {q_kcal:.2f} kcal/(h.m²)")

    # 4. pérdidas de calor en kcal/h a través de 1 m2 de pared del hogar
    A = 1  # m²
    perdidas_calor = q_kcal * A
    print(f"Pérdidas de calor Q: {perdidas_calor:.2f} kcal/h")


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
    T11 = np.linspace(t1, tc_sol, 50)


    # Capa 2: variación lineal de la temperatura
    x2 = np.linspace(e1, e1 + e2, 50)
    T2 = np.linspace(tc_sol, t2, 50)

    plt.figure(figsize=(10, 6))
    plt.plot(x1, T11, 'black', linewidth=2, linestyle='--')
    plt.plot(x1, T1, 'purple', linewidth=2, label='Magnesita (k variable - Parabólico)')
    plt.plot(x2, T2, 'cyan', linewidth=2, label='Ladrillo Rojo (k constante - Lineal)')

    # Detalles visuales
    plt.axvline(0, color='black', linestyle='--')
    plt.axvline(e1, color='black', linestyle='--')
    plt.axvline(e1 + e2, color='black', linestyle='--')
    plt.text(e1, tc_sol + tc_sol*0.1, f' {tc_sol:.1f}°C', color='black')

    # Puntos para temperaturas de los extremos
    plt.plot(0, t1, 'bo', markersize=10, label=f'Temperatura t1 = {t1} °C')  # Punto azul en x=0, y=t1
    plt.plot(e1, tc_sol, 'ro', markersize=10, label=f'Temperatura tc = {tc_sol:.2f} °C')  # Punto rojo en x= e1, y=tc
    plt.plot(e1 + e2, t2, 'go', markersize=10, label=f'Temperatura t2 = {t2} °C')  # Punto verde en x= e1+e2, y=t2

    plt.title("Distribución de Temperatura en la Pared de la Caldera")
    plt.xlabel("Espesor [m]")
    plt.ylabel("Temperatura [°C]")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()



    # --- ZOOM EN LA CAPA 2 ---
    # Ajustamos los límites para ver solo la zona donde k varía
    plt.figure(figsize=(10, 6))

    # Graficamos la curva real (parabólica)
    plt.plot(x1, T1, 'purple', linewidth=2, label='Distribución Real (Parabólica)')

    # Graficamos una línea punteada que une t2 y t3 para ver la diferencia
    plt.plot(x1, T11, 'k--', alpha=0.6, label='Referencia Lineal (k = cte)')


    plt.xlim(0 - 0.005, e1 + 0.005)
    plt.ylim( tc_sol + 1, t1 - 1)


    plt.title("Efecto de la Conductividad Variable en la Capa 1 (Zoom)")
    plt.legend()
    plt.grid(True, which='both', linestyle=':', alpha=0.5) # with='both' para mostrar cuadrícula mayor y menor
    plt.show()




# ----- PERDIDAS DE CALOR para el problema 4 -----
def ecuacion_de_calor():
    
    tc_array = fsolve(ecuacion, 500)

    # convertimos el resultado a float:
    tc_sol = float(tc_array[0])

    #Calculo del flujo de calor

    q = - k2 * (t2 - tc_sol) / e2

    print(f"Flujo de calor q: {q:.2f} W/m²")
    return q





""" 
tc_sol = fsolve(ecuacion, 500)[0]

fsolve: Es una función de la librería scipy que busca la "raíz" de una ecuación. Es decir, 
busca qué número hace que la diferencia entre el calor que sale de la capa 1 y el que entra 
a la capa 2 sea cero.

ecuacion: Es la función que definimos antes. 

fsolve le irá probando valores de temperatura hasta que q_1 = q_2.

500: Es el valor inicial (guess). Las computadoras necesitan un punto de partida para empezar
 a buscar. Como sabemos que la temperatura está entre 1100 y 50, 500 es un buen lugar para 
 empezar a "adivinar".

[0]: fsolve devuelve una lista de resultados (aunque solo sea uno). Ponemos [0] para tomar el 
primer valor de esa lista y guardarlo como un número normal en la variable tc_sol. """



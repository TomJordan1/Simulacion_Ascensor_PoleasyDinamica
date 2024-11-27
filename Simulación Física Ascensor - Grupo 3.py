"""

---Simulación de ascensor accesible basado en poleas y principios de dinámica---

                    Proyecto de Física 1 - Grupo 3
                            Ciclo: 2024-2
                            
    Universidad Nacional de Ingeniería - Facultad de Ingeniería Ambiental

"""

####
"""Cambie los parámetros y variables de estado de forma realista. Todos los cálculos se realizarán en tiempo real."""
"""


Para fines meramente demostrativos, se tomaron algunos parametros de la tesis de Pinto Yataco,
'DISEÑO DE UN ASCENSOR ELÉCTRICO CON CAPACIDAD DE 
300kg PARA EL ACCESO DE PERSONAS DISCAPACITADAS 
HASTA EL TERCER NIVEL DEL PABELLÓN DE AULAS DE LA 
FIME – UNAC'


""" 
####

import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
m_cabina = 500  # masa de la cabina (kg)
m_carga_util = 300 # masa que puede soportar la cabina (kg)
m_contrapeso = m_cabina + m_carga_util / 2  # masa del contrapeso (kg)
mR1 = 8 # masa de la polea 1 (kg)
mR2 = 10 # masa de la polea 2 (kg)
R1 = 0.32  # radio de la polea conectada al motor (m)
R2 = 0.45  # radio de la polea sin motor (m)
I1 = 0.5 * mR1 * R1**2  # momento de inercia de la polea 1 (kg*m^2)
I2 = 0.5 * mR2 * R2**2  # momento de inercia de la polea 2 (kg*m^2)
g = 9.81  # aceleración de la gravedad (m/s^2)
eficiencia_real = 0.8 # Eficiencia del motor
t_max = 4  # tiempo máximo de simulación (s)

# Función para calcular la aceleración del sistema
def calcular_aceleracion(m_cabina, m_contrapeso, g, I1, I2, R1, R2):
    a = ((m_contrapeso - m_cabina)*g*R2) / ((m_cabina + m_contrapeso)*R2 + (I2 / R2**2))
    return a

# Función para calcular la velocidad en función del tiempo
def calcular_velocidad_tiempo(v0, a, t):
    return v0 + a * t

# Función para calcular la posición en función del tiempo
def calcular_posicion_tiempo(x0, v0, a, t):
    return x0 + v0 * t + 0.5 * a * t**2

# Función para calcular el torque requerido por el motor
def calcular_torque_motor_corregido(m_cabina, R1, I1, a, g):
    torque_motor = m_cabina * R1 * (g - a) + (I1 / R1) * a
    return torque_motor

# Función para calcular la velocidad angular
def calcular_torque_motor_corregido(m_cabina, R1, I1, a, g):
    torque_motor = m_cabina * R1 * (g - a) + (I1 / R1) * a
    return torque_motor

# Función para calcular la potencia del motor
def calcular_potencia_motor(torque_motor, velocidad_angular):
    return torque_motor * velocidad_angular * eficiencia_real

# Cálculos
a = calcular_aceleracion(m_cabina, m_contrapeso, g, I1, I2, R1, R2)
v0 = 0  # velocidad inicial (m/s)
x0 = 0  # posición inicial (m)

tiempos = np.linspace(0, t_max, 100)
velocidades = [calcular_velocidad_tiempo(v0, a, t) for t in tiempos]
posiciones = [calcular_posicion_tiempo(x0, v0, a, t) for t in tiempos]
omega1_tiempos = [v / R1 for v in velocidades]
torque_motor = calcular_torque_motor_corregido(m_cabina, R1, I1, a, g)
potencias = [calcular_potencia_motor(torque_motor, omega) for omega in omega1_tiempos]

# Cálculo de la velocidad media y potencia basada en ella
v_media = velocidades[-1] / 2  # Si la velocidad inicial es 0, la velocidad media es la mitad de la final
omega_media = v_media / R1  # Velocidad angular media de la polea conectada al motor
potencia_media = torque_motor * omega_media * eficiencia_real # Potencia del motor basada en la velocidad media

# Mostrar resultados
print("Aceleración del sistema: {:.2f} m/s^2".format(a))
print("Torque requerido por el motor : {:.2f} N*m".format(torque_motor))
print("Velocidad media del sistema: {:.2f} m/s".format(v_media))
print("Velocidad angular media de la polea conectada al motor: {:.2f} rad/s".format(omega_media))
print("Potencia basada en la velocidad media: {:.2f} W".format(potencia_media))


# Visualización de resultados
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(tiempos, velocidades, label='Velocidad')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.title('Velocidad vs Tiempo')
plt.legend()
plt.grid()

plt.subplot(1, 3, 2)
plt.plot(tiempos, posiciones, label='Posición', color='green')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (m)')
plt.title('Posición vs Tiempo')
plt.legend()
plt.grid()

plt.subplot(1, 3, 3)
plt.plot(tiempos, potencias, label='Potencia del Motor', color='orange')
plt.xlabel('Tiempo (s)')
plt.ylabel('Potencia (W)')
plt.title('Potencia vs Tiempo')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


#No resultó tan complicado como parecía :´)

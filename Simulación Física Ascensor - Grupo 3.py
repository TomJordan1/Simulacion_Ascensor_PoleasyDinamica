"""

---Simulación de ascensor accesible basado en poleas y principios de dinámica---

                    Proyecto de Física 1 - Grupo 3
                            Ciclo: 2024-2
                            
    Universidad Nacional de Ingeniería - Facultad de Ingeniería Ambiental

"""

####
"""Cambie los parámetros y variables de estado de forma realista. Todos los cálculos se realizarán en tiempo real."""
####

# Parámetros iniciales
masa_cabina = 100  # Masa de la cabina en kg
masa_carga = 50  # Masa de la carga en kg (peso de los pasajeros)
masa_contrapeso = 75  # Masa del contrapeso en kg
altura_max = 5  # Altura máxima que puede alcanzar la cabina
altura_min = 0  # Altura mínima que puede alcanzar la cabina
gravedad = -9.81  # Gravedad en m/s²
fuerza_base = 150  # Fuerza base del motor en N
limite_velocidad = 2  # Límite de velocidad en m/s
coef_frenado = 0.1  # Coeficiente de frenado gradual
paso_tiempo = 0.1  # Paso de tiempo en segundos
num_poleas = 1  # Número de poleas

radio_polea = 0.2  # Radio de la polea en metros
direccion = "bajar"  # Subida o bajada
motor_activo = True  # Estado inicial del motor
limite_torque = 100  # Límite de torque en Nm
limite_potencia = 0  # Límite de potencia en W

# Variables de estado
pos_cabina = 0  # Posición inicial de la cabina en metros
vel_cabina = 0  # Velocidad inicial de la cabina en m/s
acel_cabina = 0  # Aceleración inicial de la cabina en m/s²
potencia_motor = 0  # Potencia inicial del motor
torque_motor = 0  # Torque inicial del motor

# Verificar paso de tiempo
if paso_tiempo <= 0:
    print("Advertencia: El paso de tiempo no puede ser menor o igual a cero. Se ha establecido en 1 segundo por defecto.")
    paso_tiempo = 1  # Asignar un valor por defecto

# Verificar número de poleas
if not isinstance(num_poleas, int) or num_poleas <= 0:
    print("Advertencia: El número de poleas no puede ser menor o igual a cero ni un número decimal. Se ha establecido en 1 por defecto.")
    num_poleas = 1  # Asignar un valor por defecto

# Función para calcular la fuerza del motor, considerando la carga, contrapeso y poleas
def aplicar_fuerza_motor(pos_cabina, vel_cabina, direccion):
    masa_total = masa_cabina + masa_carga  # Masa total de la cabina y la carga
    fuerza_neta_gravedad = (masa_total - masa_contrapeso) * gravedad  # Fuerza neta debido a la gravedad

    # Control de subida y bajada
    if direccion == "subir":
        fuerza_aplicada = fuerza_base + fuerza_neta_gravedad / num_poleas  # Subida
    elif direccion == "bajar":
        fuerza_aplicada = -(fuerza_base + fuerza_neta_gravedad / num_poleas)  # Bajada
    else:
        fuerza_aplicada = 0  # Por seguridad

    # Frenado en límites
    if pos_cabina >= altura_max and direccion == "subir":
        return -coef_frenado * vel_cabina  # Frenar al tope
    elif pos_cabina <= altura_min and direccion == "bajar":
        return -coef_frenado * vel_cabina  # Frenar al mínimo
    elif abs(vel_cabina) > limite_velocidad:
        return -coef_frenado * vel_cabina  # Frenado gradual
    else:
        return fuerza_aplicada  # Fuerza del motor según la dirección

### Simulación

tiempo_simulacion = 10  # Tiempo total de la simulación en segundos
n = int(tiempo_simulacion / paso_tiempo)  # Número de pasos de la simulación

for paso in range(n):  # Simular "n" pasos de tiempo
    pos_cabina_prev = pos_cabina  # Guardar posición anterior para cálculo de velocidad

    # Calcular la fuerza del motor en este paso
    fuerza_motor = aplicar_fuerza_motor(pos_cabina, vel_cabina, direccion)

    # Calcular la aceleración debido a la gravedad
    fuerza_neta_gravedad = (masa_cabina + masa_carga - masa_contrapeso) * gravedad

    # Aceleración total = (Fuerza del motor + Fuerza neta de gravedad) / masa total
    if direccion == "bajar":
        acel_cabina = (fuerza_motor + fuerza_neta_gravedad) / (masa_cabina + masa_carga)
    elif direccion == "subir":
        acel_cabina = -(fuerza_motor + fuerza_neta_gravedad) / (masa_cabina + masa_carga)
        
    # Actualizar la velocidad y posición de la cabina
    vel_cabina = vel_cabina + acel_cabina * paso_tiempo  # Velocidad
    pos_cabina = pos_cabina + vel_cabina * paso_tiempo  # Posición

    # Respetar los límites de altura
    if pos_cabina > altura_max:
        pos_cabina = altura_max
        vel_cabina = 0  # Detener al llegar al tope
    elif pos_cabina < altura_min:
        pos_cabina = altura_min
        vel_cabina = 0  # Detener al llegar a la base

    # Calcular el torque del motor
    torque_motor = fuerza_motor * radio_polea
    torque_motor = min(torque_motor, limite_torque)  # Aplicar límite de torque

    # Calcular la potencia del motor
    potencia_motor = fuerza_motor * abs(vel_cabina)
    potencia_motor = min(potencia_motor, limite_potencia)  # Aplicar límite de potencia

    # Mostrar resultados de cada paso
    print(f"Paso {paso}:")
    print(f"  Altura de la cabina: {pos_cabina:.2f} m")
    print(f"  Velocidad de la cabina: {vel_cabina:.2f} m/s")
    print(f"  Aceleración de la cabina: {acel_cabina:.2f} m/s²")
    print(f"  Fuerza aplicada por el motor: {fuerza_motor:.2f} N")
    print(f"  Potencia del motor: {potencia_motor:.2f} W (Límite: {limite_potencia} W)")
    print(f"  Torque del motor: {torque_motor:.2f} Nm (Límite: {limite_torque} Nm)")
    print(f"  Dirección: {direccion}")

    # Cambio de dirección al llegar a límites
    if pos_cabina >= altura_max and direccion == "subir":
        respuesta = input("La cabina ha alcanzado el tope. ¿Cambiar de dirección? (sí/no): ").strip().lower()
        if respuesta == "sí":
            direccion = "bajar"
            print("*** Cambiando dirección: Subiendo")
        else:
            break
    elif pos_cabina <= altura_min and direccion == "bajar":
        respuesta = input("La cabina ha alcanzado la base. ¿Cambiar de dirección? (sí/no): ").strip().lower()
        if respuesta == "sí":
            direccion = "subir"
            print("*** Cambiando dirección: Subiendo")    
        else:
            break

    # Verificar si se exceden límites
    if abs(vel_cabina) > limite_velocidad:
        print(f"  *** Frenado... Velocidad excedida: {vel_cabina:.2f} m/s")

print("Simulación completada.")


# :)

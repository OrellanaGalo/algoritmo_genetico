import random
import string
import matplotlib.pyplot as plt

FRASE_OBJETIVO = "INTELIGENCIA ARTICIAL"
TAMANIO_POBLACION = 150

# 1% de probabilidad de mutación por caracter
TASA_MUTACION = 0.01

# Cantidad de individuos en selección por torneo
TAMANIO_TORNEO = 5 
MAX_GENERACIONES = 1000

# Abecedario permitido:
ABECEDARIO = string.ascii_uppercase + " ÑÁÉÍÓÚ"

# Funcion que genera una cadena random de caracteres dentro del abecedario permitido.
def generar_individuo_aleatorio(longitud):
    return "".join(random.choice(ABECEDARIO) for _ in range(longitud))

# Compara posicion a posicion si el individuo se parece a la frase objetivo. Entre 0.0 y 1.0.
def calcular_aptitud(individuo, objetivo):
    coincidencias = sum(1 for char_ind, char_obj in zip(individuo, objetivo) if char_ind == char_obj)
    return coincidencias / len(objetivo)

# Elige 'k' cantidad de individuos al azar y devuelve el que tenga mayor cantidad de apitutd
def seleccion_torneo(poblacion, aptitudes, k=TAMANIO_TORNEO):
    aspirantes = random.sample(list(zip(poblacion, aptitudes)), k)
    aspirantes.sort(key=lambda x: x[1], reverse=True)
    return aspirantes[0][0]

# Seleccion por ruleta cuya probabilidad de elegir un individuo es proporcional a su aptitud.
def seleccion_por_ruleta(poblacion, aptitudes):
    suma_aptitudes = sum(aptitudes)
    if suma_aptitudes == 0:
        return random.choice(poblacion)
    
    punto_ruleta = random.uniform(0, suma_aptitudes)
    acumulado = 0.0
    for individuo, aptitud in zip(poblacion, aptitudes):
        acumulado += aptitud
        if acumulado >= punto_ruleta:
            return individuo
    return poblacion[-1]

# Cruzamiento, elige un punto de cruce al azar y combina los padres para crear dos hijos.
def cruzamiento(padre_1, padre_2):
    punto_cruce = random.randint(1, len(padre_1) - 1)
    hijo_1 = padre_1[:punto_cruce] + padre_2[punto_cruce:]
    hijo_2 = padre_2[:punto_cruce] + padre_1[punto_cruce:]
    return hijo_1, hijo_2

# Aplica la mutacion caracter por caracter segun la tasa de mutacion que definamos.
def mutacion(individuo, tasa_mutacion):
    individuo_mutado = list(individuo)
    for i in range(len(individuo_mutado)):
        if random.random() < tasa_mutacion:
            individuo_mutado[i] = random.choice(ABECEDARIO)
    return "".join(individuo_mutado)

def ejecutar_algoritmo_genetico():
    print("=" * 60)
    print("ALGORITMO GENÉTICO: Evolución hacia la frase objetivo")
    print(f" Frase objetivo: '{FRASE_OBJETIVO}'")
    print(f" Tamaño de población: {TAMANIO_POBLACION}")
    print(f" Tasa de mutación: {TASA_MUTACION * 100}%")
    print("=" * 60)

    longitud_objetivo = len(FRASE_OBJETIVO)
    poblacion = [generar_individuo_aleatorio(longitud_objetivo) for _ in range(TAMANIO_POBLACION)]
    historial_mejor_fitness = []
    historial_promedio_fitness = []

    # Toda la configuracion de la grafica de evolucion.
    plt.ion()
    fig, ax = plt.subplots(figsize=(11, 6))
    linea_mejor, = ax.plot([], [], label='Mejor Aptitud', color='blue', linewidth=2.5)
    linea_promedio, = ax.plot([], [], label='Aptitud Promedio', color='orange', linewidth=1.8, linestyle='--')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.05)
    ax.set_title(f"Evolución de frase objetivo: '{FRASE_OBJETIVO}'", fontsize=14, fontweight='bold')
    ax.set_xlabel('Generacion', fontsize=12)
    ax.set_ylabel('Aptitud', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', fontsize=10)

    texto_pantalla = ax.text(0.02, 0.45, "", transform=ax.transAxes, fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0f0f0", edgecolor="#cccccc", alpha=0.9))
    
    generacion = 0
    mejor_individuo = ""
    mejor_fitness = 0.0

    # Bucle del algoritmo genetico
    for generacion in range(1, MAX_GENERACIONES + 1):
        aptitudes = [calcular_aptitud(ind, FRASE_OBJETIVO) for ind in poblacion]
        
        idx_mejor = max(range(len(aptitudes)), key=lambda i: aptitudes[i])
        mejor_actual = poblacion[idx_mejor]
        fitness_actual = aptitudes[idx_mejor]
        promedio_actual = sum(aptitudes) / len(aptitudes)
        
        historial_mejor_fitness.append(fitness_actual)
        historial_promedio_fitness.append(promedio_actual)
        
        if fitness_actual > mejor_fitness:
            mejor_fitness = fitness_actual
            mejor_individuo = mejor_actual

        if generacion % 5 == 0 or fitness_actual == 1.0:
            print(f"Gen {generacion:03d} | Mejor: '{mejor_actual}' | Fitness: {fitness_actual*100:5.1f}% | Prom: {promedio_actual*100:5.1f}%")

        linea_mejor.set_data(range(len(historial_mejor_fitness)), historial_mejor_fitness)
        linea_promedio.set_data(range(len(historial_promedio_fitness)), historial_promedio_fitness)
        
        ax.set_xlim(0, max(50, len(historial_mejor_fitness) + 5))
        
        info_str = (f"Generación: {generacion}\n"
                    f"Mejor Cadena: '{mejor_actual}'\n"
                    f"Aptitud Actual: {fitness_actual*100:.1f}%\n"
                    f"Aptitud Promedio: {promedio_actual*100:.1f}%")
        texto_pantalla.set_text(info_str)
        
        plt.draw()
        plt.pause(0.01)

        if fitness_actual == 1.0:
            print("\n" + "=" * 60)
            print(f" OBJETIVO ALCANZADO EN LA GENERACIÓN {generacion}")
            print(f" Resultado Final: '{mejor_actual}'")
            print("=" * 60)
            break

        nueva_poblacion = [mejor_actual]
        
        # Generar nueva poblacion mediante seleccion, cruzamiento y mutacion
        while len(nueva_poblacion) < TAMANIO_POBLACION:
            padre1 = seleccion_torneo(poblacion, aptitudes)
            padre2 = seleccion_torneo(poblacion, aptitudes)
            
            hijo1, hijo2 = cruzamiento(padre1, padre2)
            
            hijo1 = mutacion(hijo1, TASA_MUTACION)
            hijo2 = mutacion(hijo2, TASA_MUTACION)
            
            nueva_poblacion.extend([hijo1, hijo2])
            
        poblacion = nueva_poblacion[:TAMANIO_POBLACION]

    plt.ioff()
    fig.savefig("grafico_evolucion.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    ejecutar_algoritmo_genetico()
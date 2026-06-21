import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importamos las funciones estocásticas que creamos en el paso anterior
from model_sir import calcular_nuevos_infectados, calcular_nuevos_recuperados

def ejecutar_simulacion_estocastica(poblacion_total, infectados_iniciales, dias, beta, gamma):
    # Inicializamos los arreglos para guardar el historial diario
    S = np.zeros(dias)
    I = np.zeros(dias)
    R = np.zeros(dias)
    Tiempo = np.arange(dias)
    
    # Condiciones iniciales
    I[0] = infectados_iniciales
    R[0] = 0
    S[0] = poblacion_total - infectados_iniciales
    
    # Bucle temporal discreto (Día con día)
    for t in range(1, dias):
        S_actual = S[t-1]
        I_actual = I[t-1]
        
        # Procesos Estocásticos mediante Distribución Binomial
        nuevos_contagios = calcular_nuevos_infectados(S_actual, I_actual, poblacion_total, beta)
        nuevas_recuperaciones = calcular_nuevos_recuperados(I_actual, gamma)
        
        # Dinámica del proceso (Ecuaciones de actualización de estado)
        S[t] = S_actual - nuevos_contagios
        I[t] = I_actual + nuevos_contagios - nuevas_recuperaciones
        R[t] = R[t-1] + nuevas_recuperaciones
        
        # Control para evitar valores negativos por fluctuación aleatoria
        if S[t] < 0: S[t] = 0
        if I[t] < 0: I[t] = 0
        
    return Tiempo, S, I, R

def generar_y_guardar_graficos(Tiempo, S, I, R):
    # Configuración de estilo estético para el reporte
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    # Graficar las curvas de la simulación
    plt.plot(Tiempo, S, label='Susceptibles (S)', color='blue', lw=2)
    plt.plot(Tiempo, I, label='Infectados (I)', color='red', lw=2.5)
    plt.plot(Tiempo, R, label='Recuperados (R)', color='green', lw=2)
    
    plt.title('Simulación Estocástica de la Propagación del COVID-19 (Modelo SIR)', fontsize=14, fontweight='bold')
    plt.xlabel('Días (Tiempo Discreto $t$)', fontsize=12)
    plt.ylabel('Número de Individuos', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    
    # Definir la ruta de guardado en la carpeta output/
    ruta_output = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "curva_sir_simulado.png"))
    plt.savefig(ruta_output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Gráfico de la simulación guardado con éxito en: output/curva_sir_simulado.png")

if __name__ == "__main__":
    # Parámetros base de prueba para la simulación
    POBLACION_N = 100000          # Tamaño de la población muestra
    INFECTADOS_I0 = 100           # Pacientes cero iniciales
    DIAS_SIMULACION = 120         # Marco de tiempo del protocolo
    
    BETA = 0.28                   # Tasa media de transmisión/contacto diario
    GAMMA = 1/14                  # Tasa diaria de recuperación (aprox. 14 días enfermo)
    
    print("Iniciando simulación del proceso estocástico...")
    
    # Ejecución
    T, S, I, R = ejecutar_simulacion_estocastica(
        poblacion_total=POBLACION_N, 
        infectados_iniciales=INFECTADOS_I0, 
        dias=DIAS_SIMULACION, 
        beta=BETA, 
        gamma=GAMMA
    )
    
    # Generar salida visual
    generar_y_guardar_graficos(T, S, I, R)
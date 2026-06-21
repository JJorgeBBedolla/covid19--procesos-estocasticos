import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importamos la función de simulación que ya construiste
from simulation import ejecutar_simulacion_estocastica

def analizar_multiples_simulaciones(num_simulaciones=100):
    # Parámetros estables del modelo
    POBLACION_N = 100000
    INFECTADOS_I0 = 100
    DIAS_SIMULACION = 120
    BETA = 0.28
    GAMMA = 1/14
    
    # Listas para almacenar las métricas de interés de cada simulación
    picos_infectados = []
    dias_del_pico = []
    
    print(f"Corriendo {num_simulaciones} simulaciones estocásticas para el análisis cuantitativo...")
    
    for i in range(num_simulaciones):
        T, S, I, R = ejecutar_simulacion_estocastica(
            POBLACION_N, INFECTADOS_I0, DIAS_SIMULACION, BETA, GAMMA
        )
        # Encontrar el valor máximo de infectados y el día en que ocurrió
        pico_maximo = np.max(I)
        dia_pico = np.argmax(I)
        
        picos_infectados.append(pico_maximo)
        dias_del_pico.append(dia_pico)
        
    # --- PASO 4.1: CALCULAR ESTADÍSTICAS RELEVANTES ---
    media_pico = np.mean(picos_infectados)
    varianza_pico = np.var(picos_infectados)
    desviacion_pico = np.std(picos_infectados)
    
    media_dia = np.mean(dias_del_pico)
    
    print("\n==================================================")
    print("      RESULTADOS ESTADÍSTICOS DEL MODELO          ")
    print("==================================================")
    print(f"Media del pico máximo de infectados: {media_pico:.2f} personas")
    print(f"Varianza del pico de infectados: {varianza_pico:.2f}")
    print(f"Desviación estándar del pico: {desviacion_pico:.2f} personas")
    print(f"Día promedio en el que se alcanza el pico: Día {media_dia:.1f}")
    print("==================================================\n")
    
    # --- PASO 4.2: VISUALIZAR LOS DATOS (HISTOGRAMA) ---
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(9, 5))
    
    # Histograma con curva de densidad (KDE)
    sns.histplot(picos_infectados, kde=True, color="purple", bins=15, edgecolor="black")
    
    # Línea vertical indicando la media
    plt.axvline(media_pico, color="red", linestyle="--", linewidth=2, label=f"Media: {media_pico:.1f}")
    
    plt.title("Distribución de Frecuencias del Pico Máximo de Infectados", fontsize=13, fontweight='bold')
    plt.xlabel("Tamaño del Pico Máximo (Número de personas simultáneamente enfermas)", fontsize=11)
    plt.ylabel("Frecuencia (Número de simulaciones)", fontsize=11)
    plt.legend()
    
    # Guardar gráfico en output/
    ruta_histograma = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "histograma_contagios.png"))
    plt.savefig(ruta_histograma, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Histograma de distribución guardado en: output/histograma_contagios.png")

if __name__ == "__main__":
    analizar_multiples_simulaciones()
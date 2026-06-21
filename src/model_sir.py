import numpy as np

def calcular_nuevos_infectados(S_actual, I_actual, N, beta):
    """
    Modela el proceso estocástico de contagio.
    Utiliza una distribución Binomial para calcular cuántos susceptibles 
    pasan al estado de Infectados basándose en la probabilidad de contacto diario.
    """
    if N == 0 or I_actual == 0:
        return 0
        
    # Probabilidad de que un individuo susceptible se contamine en el día t
    p_contagio = beta * (I_actual / N)
    
    # Asegurar que la probabilidad no exceda 1
    p_contagio = min(max(p_contagio, 0.0), 1.0)
    
    # Proceso estocástico: número de éxitos (contagios) en S_actual ensayos
    nuevos_casos = np.random.binomial(n=int(S_actual), p=p_contagio)
    return nuevos_casos

def calcular_nuevos_recuperados(I_actual, gamma):
    """
    Modela el proceso estocástico de recuperación.
    Cada individuo infectado tiene una probabilidad diaria fija 'gamma' de recuperarse.
    El tiempo total sigue una distribución geométrica.
    """
    if I_actual == 0:
        return 0
        
    # Proceso estocástico: cada infectado lanza una moneda para ver si se recupera hoy
    nuevos_recuperados = np.random.binomial(n=int(I_actual), p=gamma)
    return nuevos_recuperados

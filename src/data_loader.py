import os
import shutil
import kagglehub
import pandas as pd

def descargar_y_organizar_datos():
    print("Descargando dataset desde Kaggle...")
    # Descarga la última versión del dataset usando kagglehub
    path_temporal = kagglehub.dataset_download("sudalairajkumar/novel-corona-virus-2019-dataset")
    print(f"Dataset descargado temporalmente en: {path_temporal}")
    
    # Definimos la ruta de destino dentro de la arquitectura de nuestro proyecto (carpeta data)
    ruta_destino = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    
    # Buscamos el archivo principal de series de tiempo (normalmente se llama 'covid_19_data.csv')
    # e intentamos moverlo a nuestra carpeta 'data/' para tenerlo localmente.
    for archivo in os.listdir(path_temporal):
        if archivo.endswith(".csv"):
            ruta_archivo_origen = os.path.join(path_temporal, archivo)
            ruta_archivo_destino = os.path.join(ruta_destino, archivo)
            
            # Copiar el archivo CSV a nuestra carpeta del proyecto
            shutil.copy(ruta_archivo_origen, ruta_archivo_destino)
            print(f"Archivo copiado con éxito: data/{archivo}")

def cargar_datos_principales():
    """Lee el archivo CSV principal una vez guardado en la carpeta data"""
    ruta_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "covid_19_data.csv"))
    if os.path.exists(ruta_csv):
        df = pd.read_csv(ruta_csv)
        return df
    else:
        raise FileNotFoundError("El archivo covid_19_data.csv no se encuentra en la carpeta data. Ejecuta primero la descarga.")

if __name__ == "__main__":
    # Si ejecutas este archivo directamente, se descargarán los datos
    descargar_y_organizar_datos()
    
    # Verificamos la carga mostrando las primeras filas
    try:
        datos = cargar_datos_principales()
        print("\n--- Vista previa de los datos cargados con éxito ---")
        print(datos.head())
    except Exception as e:
        print(f"Error al verificar la carga: {e}")
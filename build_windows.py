import os
import sys
import shutil

def build_windows():
    # Verificar que estamos en Windows
    if sys.platform != 'win32':
        print("Este script debe ejecutarse en Windows para crear el ejecutable.")
        return

    # Instalar dependencias necesarias
    os.system('pip install pyinstaller')
    os.system('pip install pandas')

    # Limpiar directorios anteriores
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Crear el ejecutable
    os.system('pyinstaller --onefile --windowed --name "NormalizadorCSV" app.py')

    # Copiar archivos necesarios
    if os.path.exists('dist/NormalizadorCSV.exe'):
        print("\n¡Compilación exitosa!")
        print("El ejecutable se encuentra en la carpeta 'dist'")
        print("\nPara distribuir la aplicación, necesitarás:")
        print("1. El archivo 'dist/NormalizadorCSV.exe'")
        print("2. La carpeta 'dist/NormalizadorCSV' (si existe)")
    else:
        print("\nError: No se pudo crear el ejecutable")

if __name__ == "__main__":
    build_windows() 

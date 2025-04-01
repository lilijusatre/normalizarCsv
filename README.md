# Normalizador de CSV

Una aplicación de escritorio para normalizar archivos CSV, especialmente
diseñada para procesar archivos de reseñas con IDs de reserva.

## Características

- Interfaz gráfica intuitiva
- Limpieza de espacios extra en texto
- Unión inteligente de comentarios relacionados
- Detección automática de IDs de reserva
- Barra de progreso en tiempo real
- Manejo robusto de errores

## Requisitos

- Python 3.x
- pandas
- tkinter (incluido con Python)

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/lilijusatre/normalizarCsv.git
```

2. Instala las dependencias:

```bash
pip install pandas
```

## Uso

1. Ejecuta la aplicación:

```bash
python3 app.py
```

2. Usa la interfaz gráfica para:
   - Cargar un archivo CSV
   - Seleccionar opciones de normalización
   - Procesar y guardar el archivo normalizado

## Opciones de Normalización

- **Limpiar espacios extra**: Elimina espacios innecesarios al inicio y final de
  cada campo
- **Unir comentarios relacionados**: Combina comentarios que pertenecen al mismo
  registro

## Estructura del Archivo CSV

El archivo CSV debe contener:

- IDs de reserva (números de 8-20 dígitos)
- Una columna "Overall review" (opcional, para comentarios)
- Campos adicionales según necesidad

## Crear Ejecutable para Windows

Para crear un ejecutable (.exe) para Windows:

1. Asegúrate de tener Python instalado en Windows
2. Clona este repositorio en Windows
3. Ejecuta el script de compilación:

```bash
python build_windows.py
```

El ejecutable se creará en la carpeta `dist` con el nombre
`NormalizadorCSV.exe`.

### Requisitos para Compilación en Windows

- Windows 10 o superior
- Python 3.x
- pip (incluido con Python)

## Licencia

[Tu licencia aquí]

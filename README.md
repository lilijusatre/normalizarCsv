# Normalizador de CSV

## Descripción

Herramienta para normalizar y limpiar archivos CSV de manera sencilla.

## Características

- Interfaz gráfica intuitiva
- Limpieza de espacios extra en texto
- Unión inteligente de comentarios relacionados
- Detección automática de IDs de reserva
- Conserva máximo detalle
- Sin conocimientos técnicos requeridos

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

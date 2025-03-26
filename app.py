import sys
import os
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class NormalizadorCSV:
    def __init__(self, master):
        self.master = master
        master.title("Normalizador de Datos CSV")
        master.geometry("600x500")
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=('Arial', 10))
        self.style.configure("TLabel", font=('Arial', 12))
        
        # Marco principal
        self.frame = ttk.Frame(master, padding="20 20 20 20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión de grid
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        # Título
        self.titulo = ttk.Label(
            self.frame, 
            text="Normalizador de Datos CSV", 
            font=('Arial', 16, 'bold')
        )
        self.titulo.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Botón de cargar archivo
        self.btn_cargar = ttk.Button(
            self.frame, 
            text="Cargar Archivo CSV", 
            command=self.cargar_archivo
        )
        self.btn_cargar.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Etiqueta de archivo seleccionado
        self.label_archivo = ttk.Label(
            self.frame, 
            text="Ningún archivo seleccionado", 
            foreground="gray",
            wraplength=500
        )
        self.label_archivo.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame para opciones
        self.frame_opciones = ttk.LabelFrame(self.frame, text="Opciones de Normalización", padding="10 10 10 10")
        self.frame_opciones.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Opciones de normalización
        self.var_limpiar_espacios = tk.BooleanVar(value=True)
        self.check_espacios = ttk.Checkbutton(
            self.frame_opciones,
            text="Limpiar espacios extra",
            variable=self.var_limpiar_espacios
        )
        self.check_espacios.grid(row=0, column=0, sticky=tk.W)
        
        self.var_unir_comentarios = tk.BooleanVar(value=True)
        self.check_comentarios = ttk.Checkbutton(
            self.frame_opciones,
            text="Unir comentarios relacionados",
            variable=self.var_unir_comentarios
        )
        self.check_comentarios.grid(row=1, column=0, sticky=tk.W)
        
        # Botón de normalizar
        self.btn_normalizar = ttk.Button(
            self.frame, 
            text="Normalizar Datos", 
            command=self.normalizar_datos,
            state=tk.DISABLED
        )
        self.btn_normalizar.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(
            self.frame, 
            orient="horizontal", 
            length=400, 
            mode="determinate"
        )
        self.progreso.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Etiqueta de estado
        self.label_estado = ttk.Label(
            self.frame,
            text="",
            foreground="gray"
        )
        self.label_estado.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Variable para almacenar ruta del archivo
        self.ruta_archivo = None
        
    def actualizar_estado(self, mensaje, color="gray"):
        self.label_estado.config(text=mensaje, foreground=color)
        self.master.update_idletasks()
    
    def cargar_archivo(self):
        # Abrir diálogo para seleccionar archivo
        self.ruta_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")]
        )
        
        if self.ruta_archivo:
            try:
                # Verificar que el archivo se puede leer
                df = pd.read_csv(self.ruta_archivo, nrows=1)
                
                # Actualizar etiqueta con nombre de archivo y tamaño
                nombre_archivo = os.path.basename(self.ruta_archivo)
                tamaño = os.path.getsize(self.ruta_archivo) / 1024  # KB
                info_archivo = f"Archivo: {nombre_archivo}\nTamaño: {tamaño:.1f} KB"
                self.label_archivo.config(text=info_archivo, foreground="black")
                
                # Habilitar botón de normalizar
                self.btn_normalizar.config(state=tk.NORMAL)
                self.actualizar_estado("Archivo cargado correctamente", "green")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")
                self.ruta_archivo = None
                self.label_archivo.config(text="Error al cargar el archivo", foreground="red")
    
    def normalizar_datos(self):
        if not self.ruta_archivo:
            messagebox.showerror("Error", "Por favor, seleccione un archivo CSV")
            return
        
        try:
            # Inicializar progreso
            self.progreso["value"] = 0
            self.actualizar_estado("Leyendo archivo...")
            
            # Leer archivo CSV
            df = pd.read_csv(self.ruta_archivo, encoding='utf-8')
            total_filas = len(df)
            
            # Funciones de normalización
            def es_reservation_id(valor):
                return bool(re.match(r'^\d{8,20}$', str(valor).strip()))
            
            def es_comentario_significativo(texto):
                if pd.isna(texto) or not isinstance(texto, str):
                    return False
                
                texto = texto.strip()
                return (
                    len(texto) > 5 and
                    bool(re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]{3,}', texto)) and
                    not es_reservation_id(texto)
                )
            
            # Contenedor para datos normalizados
            datos_normalizados = []
            registro_actual = None
            
            # Normalizar datos
            for i, (_, fila) in enumerate(df.iterrows()):
                # Actualizar progreso
                self.progreso["value"] = (i + 1) / total_filas * 100
                self.actualizar_estado(f"Procesando fila {i + 1} de {total_filas}...")
                
                # Convertir fila a lista
                fila_lista = list(fila)
                
                # Limpiar espacios si está activada la opción
                if self.var_limpiar_espacios.get():
                    fila_lista = [str(val).strip() if isinstance(val, str) else val for val in fila_lista]
                
                # Detectar nuevo registro
                ids_reserva = [val for val in fila_lista if es_reservation_id(val)]
                
                if ids_reserva:
                    # Guardar registro anterior
                    if registro_actual:
                        datos_normalizados.append(registro_actual)
                    registro_actual = fila_lista.copy()
                
                elif registro_actual is not None and self.var_unir_comentarios.get():
                    # Extraer y unir comentarios
                    comentarios = [str(val) for val in fila_lista if es_comentario_significativo(val)]
                    if comentarios:
                        if 'Overall review' in df.columns:
                            idx = df.columns.get_loc('Overall review')
                            registro_actual[idx] = f"{registro_actual[idx]} {' '.join(comentarios)}"
                        else:
                            registro_actual.extend(comentarios)
            
            # Agregar último registro
            if registro_actual:
                datos_normalizados.append(registro_actual)
            
            # Convertir a DataFrame
            self.actualizar_estado("Creando archivo normalizado...")
            df_normalizado = pd.DataFrame(datos_normalizados, columns=df.columns)
            
            # Guardar archivo normalizado
            ruta_guardado = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                initialfile="normalizado_" + os.path.basename(self.ruta_archivo)
            )
            
            if ruta_guardado:
                df_normalizado.to_csv(ruta_guardado, index=False, encoding='utf-8')
                self.actualizar_estado("¡Normalización completada!", "green")
                messagebox.showinfo(
                    "Éxito", 
                    f"Archivo normalizado guardado en:\n{ruta_guardado}\n\n"
                    f"Registros procesados: {len(df_normalizado)}"
                )
            else:
                self.actualizar_estado("Operación cancelada", "orange")
            
        except Exception as e:
            self.actualizar_estado("Error durante la normalización", "red")
            messagebox.showerror("Error", str(e))
        
        finally:
            # Resetear progreso
            self.progreso["value"] = 0

def main():
    root = tk.Tk()
    app = NormalizadorCSV(root)
    root.mainloop()

if __name__ == "__main__":
    main()

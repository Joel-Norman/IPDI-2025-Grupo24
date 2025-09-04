from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# Variables globales
imagen = None
imagen_mod = None
img_tk = None

# Funciones
def abrir_imagen():
    global imagen, imagen_mod
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
    if ruta:
        imagen = Image.open(ruta).convert("RGB")
        imagen_mod = imagen.copy()
        mostrar_imagen(imagen_mod)
        print(f"Imagen '{ruta}' abierta. Tamaño: {imagen.size}")

def modificar_pixeles():
    global imagen_mod
    if imagen_mod is None:
        messagebox.showwarning("Aviso", "No hay imagen cargada.")
        return
    
    pixeles = imagen_mod.load()
    ancho, alto = imagen_mod.size

    for x in range(ancho):
        for y in range(alto):
            r, g, b = pixeles[x, y]
            pixeles[x, y] = (255 - r, 255 - g, 255 - b)
    
    mostrar_imagen(imagen_mod)
    print("Colores de la imagen invertidos.")

def guardar_imagen():
    global imagen_mod
    if imagen_mod is None:
        messagebox.showwarning("Aviso", "No hay imagen para guardar.")
        return
    
    ruta_salida = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
    if ruta_salida:
        imagen_mod.save(ruta_salida)
        print(f"Imagen guardada como '{ruta_salida}'")

def mostrar_imagen(imagen_a_mostrar):
    global img_tk
    img_tk = ImageTk.PhotoImage(imagen_a_mostrar)
    etiqueta.config(image=img_tk)
    etiqueta.image = img_tk  # mantener referencia

# Crear ventana principal
root = tk.Tk()
root.title("Visor de Imágenes")

# Panel de botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Abrir Imagen", command=abrir_imagen).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Invertir Colores", command=modificar_pixeles).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Guardar Imagen", command=guardar_imagen).pack(side=tk.LEFT, padx=5)

# Etiqueta para mostrar la imagen
etiqueta = tk.Label(root)
etiqueta.pack(pady=10)

root.mainloop()
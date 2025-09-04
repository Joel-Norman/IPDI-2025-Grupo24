from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Variables globales
imagen = None
imagen_mod = None
img_tk = None
a = 1.0  # coeficiente de luminancia
b = 1.0  # coeficiente de saturación

# Funciones
def abrir_imagen():
    global imagen, imagen_mod
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
    if ruta:
        imagen = Image.open(ruta).convert("RGB")
        imagen_mod = imagen.copy()
        mostrar_imagen(imagen_mod)
        print(f"Imagen '{ruta}' abierta. Tamaño: {imagen.size}")

def aplicar_yiq(im, coef_lum=1.0, coef_sat=1.0):
    """Aplica cambios de luminancia y saturación usando YIQ"""
    if im is None:
        return None
    
    arr = np.array(im, dtype=np.float32) / 255.0  # Normalizar a 0-1
    R = arr[:,:,0]
    G = arr[:,:,1]
    B = arr[:,:,2]

    # Matriz RGB -> YIQ
    Y = 0.299*R + 0.587*G + 0.114*B
    I = 0.596*R - 0.275*G - 0.321*B
    Q = 0.212*R - 0.523*G + 0.311*B

    # Ajustar luminancia y saturación
    Y = coef_lum * Y
    I = coef_sat * I
    Q = coef_sat * Q

    # Chequear rangos
    Y = np.clip(Y, 0, 1)
    I = np.clip(I, -0.5957, 0.5957)
    Q = np.clip(Q, -0.5226, 0.5226)

    # Matriz YIQ -> RGB
    Rn = Y + 0.956*I + 0.621*Q
    Gn = Y - 0.272*I - 0.647*Q
    Bn = Y - 1.106*I + 1.703*Q

    # Chequear rangos 0-1
    Rn = np.clip(Rn, 0, 1)
    Gn = np.clip(Gn, 0, 1)
    Bn = np.clip(Bn, 0, 1)

    # Convertir a bytes 0-255
    arr_mod = np.stack([Rn, Gn, Bn], axis=2) * 255
    return Image.fromarray(arr_mod.astype(np.uint8))

def actualizar_imagen(val=None):
    global imagen_mod, a, b
    if imagen is None:
        return
    a = slider_lum.get()
    b = slider_sat.get()
    imagen_mod = aplicar_yiq(imagen, a, b)
    mostrar_imagen(imagen_mod)
    print(f"Luminancia: {a:.2f}, Saturación: {b:.2f}")

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
root.title("Manipulación de Luminancia y Saturación (YIQ)")

# Panel de botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Abrir Imagen", command=abrir_imagen).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Guardar Imagen", command=guardar_imagen).pack(side=tk.LEFT, padx=5)

# Sliders para luminancia y saturación
frame_sliders = tk.Frame(root)
frame_sliders.pack(pady=10)

tk.Label(frame_sliders, text="Luminancia (a)").grid(row=0, column=0)
slider_lum = tk.Scale(frame_sliders, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, length=300, command=actualizar_imagen)
slider_lum.set(1.0)
slider_lum.grid(row=0, column=1)

tk.Label(frame_sliders, text="Saturación (b)").grid(row=1, column=0)
slider_sat = tk.Scale(frame_sliders, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, length=300, command=actualizar_imagen)
slider_sat.set(1.0)
slider_sat.grid(row=1, column=1)

# Etiqueta para mostrar la imagen
etiqueta = tk.Label(root)
etiqueta.pack(pady=10)

root.mainloop()
# Importar las clases Image y ImageTk desde el módulo PIL (Python Imaging Library)
from PIL import Image, ImageTk

# Definir una función llamada 'leer_imagen' que toma la ruta de un archivo de imagen y un tamaño como parámetros
def leer_imagen(path, size):
    # Abrir la imagen en la ruta especificada, redimensionarla según el tamaño dado y convertirla a PhotoImage
    return ImageTk.PhotoImage(Image.open(path).resize(size, resample=Image.BICUBIC))

# Definir una función llamada 'centrar_ventana' que toma una ventana y las dimensiones de la aplicación como parámetros
def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    # Obtener el ancho y alto de la pantalla
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    
    # Calcular las coordenadas x e y para centrar la ventana en la pantalla
    x = int((pantall_ancho / 2) - (aplicacion_ancho / 2))
    y = int((pantall_largo / 2) - (aplicacion_largo / 2))
    
    # Establecer la geometría de la ventana con las coordenadas calculadas
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

# Se importan las librerías necesarias para construir la interfaz gráfica (tkinter),
# mostrar cuadros de mensaje (messagebox), trabajar con imágenes (PIL),
# y una clase (MasterPanel) desde un módulo llamado form_master.
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from forms.form_master import MasterPanel

# Se define una clase llamada App para encapsular toda la funcionalidad de la aplicación.
class App:

    # Este método se llama cuando se presiona el botón "Iniciar sesión".
    # Verifica las credenciales ingresadas y muestra mensajes de error si es necesario.
    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()

        # Validar que ambos campos no estén vacíos
        if not usu or not password:
            self.mostrar_error("Error de inicio de sesión", "Por favor, completa ambos campos.")
        elif usu == 'root' and password == '1234':
            self.ventana.destroy()
            master_panel = MasterPanel(tk.Toplevel())
        else:
            self.mostrar_error("Error de inicio de sesión", "Usuario o contraseña incorrectos")

    # Este método muestra un cuadro de diálogo de error con un título y un mensaje.
    def mostrar_error(self, title, message):
        messagebox.showerror(title, message)

    # Se utiliza para manejar la tecla "Enter".
    # Si la tecla Enter se presiona en el campo de usuario, pasa el foco al campo de contraseña.
    # Si se presiona en el campo de contraseña, verifica las credenciales.
    def funcEnter(self, event):
        # Esta función se llamará cuando se presione Enter en un Entry
        if event.widget == self.usuario:
            self.password.focus_set()
        elif event.widget == self.password:
            self.verificar()

    # Cambia entre mostrar y ocultar la contraseña en el campo de contraseña cuando se hace clic en un botón de ojo.
    def toggle_password(self):
        current_show_value = self.password.cget('show')
        if current_show_value == '':
            self.password.config(show='•')
            self.eye_button.config(image=self.open_eye_image)
        else:
            self.password.config(show='')
            self.eye_button.config(image=self.close_eye_image)

    # Cambia el fondo y el color del texto del botón "Iniciar sesión" cuando el ratón pasa sobre él.
    def on_hover(self, event):
        self.inicio.config(bg='#e84e5f', fg='#ffffff')

    def on_leave(self, event):
        self.inicio.config(bg='#da3e4d', fg='#f6f6f8')

    # Constructor de la clase
    def __init__(self):
        # Configuración de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de sesión')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)

        # Centrar la ventana en la pantalla
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x_position = (screen_width - 800) // 2
        y_position = (screen_height - 500) // 2
        self.ventana.geometry(f'800x500+{x_position}+{y_position}')

        # Configuración del ícono de la ventana
        self.ventana.iconbitmap('./img/icon.ico')

        # Cargar y mostrar un logo en la ventana
        logo = ImageTk.PhotoImage(Image.open("./img/logo.png").resize((200, 200)))
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, bg='#D72D3D')
        frame_logo.pack(side='left', expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#D72D3D')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Configuración de los elementos de la interfaz
        frame_derecho = tk.Frame(self.ventana, bd=0, width=50, relief=tk.SOLID, padx=10, bg='#D72D3D')
        frame_derecho.pack(side='right', expand=tk.NO, fill=tk.BOTH)

        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#F0F0F0')
        frame_form.pack(side='right', expand=tk.YES, fill=tk.BOTH)

        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side='top', fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=('Arial', 30), fg='#666a88', bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#f0f0f0')
        frame_form_fill.pack(side='bottom', expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text='Usuario', font=('Arial', 14), fg="#5e617d", bg='#f0f0f0', anchor='w')
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=20)
        self.usuario = ttk.Entry(frame_form_fill, font=('Arial', 14))
        self.usuario.config(foreground='#7a7e9b')
        self.usuario.pack(fill=tk.X, padx=20, pady=0)
        self.usuario.bind('<Return>', self.funcEnter)  # Vincular la tecla Enter a funcEnter

        etiqueta_password = tk.Label(frame_form_fill, text='Contraseña', font=('Arial', 14), fg='#5e617d', bg='#f0f0f0', anchor='w')
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Arial', 14), show="•")
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(foreground="#7a7e9b")

        # Configuración de botón y eventos
        self.open_eye_image = ImageTk.PhotoImage(Image.open('./img/eye.png').resize((20, 20)))
        self.close_eye_image = ImageTk.PhotoImage(Image.open('./img/eye_close.png').resize((20, 20)))

        self.eye_button = tk.Button(frame_form_fill, image=self.open_eye_image, command=self.toggle_password, bd=0, bg='#FFFFFF')
        self.eye_button.place(relx=1.0, rely=0.4, anchor='ne', x=-30, y=7)

        self.inicio = tk.Button(frame_form_fill, text='Iniciar sesión', cursor='hand2', font=('Arial', 15, BOLD),
                                bg='#da3e4d', bd=0, fg='#f6f6f8', command=self.verificar)
        self.inicio.pack(fill=tk.X, padx=20, pady=20)

        # Vincular eventos de ratón al botón de inicio de sesión
        self.inicio.bind('<Enter>', self.on_hover)
        self.inicio.bind('<Leave>', self.on_leave)

        # Vincular eventos de teclado a la ventana principal y al campo de usuario
        self.ventana.bind('<Return>', self.funcEnter)
        self.usuario.bind('<Return>', self.funcEnter)  # Vincular la tecla Enter a funcEnter

        # Establecer el foco inicial en el campo de usuario
        self.usuario.focus_set()

        # Iniciar el bucle principal de la interfaz gráfica
        self.ventana.mainloop()

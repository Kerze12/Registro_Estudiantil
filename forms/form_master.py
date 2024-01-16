import tkinter as tk
from tkinter.font import BOLD
import util.generic as utl  # Importar un módulo personalizado llamado 'generic' desde el paquete 'util'.
from database import *  # Importar todas las funciones y clases desde el módulo 'database'.
from tkinter import Tk, Label, Entry, Button, StringVar, Toplevel, ttk, messagebox, Frame, CENTER

# Definir las variables de color globalmente
color_principal = '#da3e4d'
color_fondo = '#da3e4d'
color_botones = '#0051C8'
color_texto_botones = '#ffffff'
color_bordes = '#d22d3d'

# Crear una clase llamada 'MasterPanel'
class MasterPanel:
    def __init__(self, master):
        # Configuración de la ventana principal
        self.ventana = master
        self.ventana.title('REGISTRO DE ESTUDIANTES')
        self.ventana.geometry('1200x600')
        self.ventana.config(background=color_fondo)

        # Estructura de los marcos
        frame_left = Frame(self.ventana, width=15, height=600, bg='#d22d3e')  # Marco izquierdo con fondo rojo.
        frame_left.pack(side=tk.LEFT)

        frame_right = Frame(self.ventana, width=15, height=600, bg='#d22d3e')  # Marco derecho con fondo rojo.
        frame_right.pack(side=tk.RIGHT)

        frame_top = Frame(self.ventana, width=1200, height=10, bg='#d22d3e')  # Marco superior con fondo rojo.
        frame_top.pack(side=tk.TOP)

        frame_bottom = Frame(self.ventana, width=1200, height=10, bg='#d22d3e')  # Marco inferior con fondo rojo.
        frame_bottom.pack(side=tk.BOTTOM)

        # Ajustes adicionales de la ventana
        self.ventana.update()
        window_width = 1200
        window_height = 600
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.ventana.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')
        self.ventana.iconbitmap('./img/icon.ico')  # Establecer el ícono de la ventana.
        self.ventana.resizable(False, False)

        # Diccionario para almacenar colores originales de los botones durante el cambio de estado.
        self.original_colors = {}
        
        # Inicializar la interfaz gráfica
        self.label()
        self.entry_widgets()
        self.buttons()
        self.draw_list("")


    def on_hover(self, event):
        # Cambiar los colores de fondo y texto cuando el ratón entra en el botón.
        widget = event.widget
        self.original_colors[widget] = (widget.cget("bg"), widget.cget("fg"))
        widget.config(bg='#0059dc', fg='#ffffff')

    def on_leave(self, event):
        # Restaurar los colores originales cuando el ratón sale del botón.
        widget = event.widget
        original_colors = self.original_colors.get(widget, (color_botones, color_texto_botones))
        widget.config(bg=original_colors[0], fg=original_colors[1])

    def label(self):
        # Crear etiquetas para diferentes campos.
        campos = ['Nombre', 'Materia', 'Nota', 'Jornada', 'Estado']
        posiciones = [(80, 25), (80, 100), (390, 100), (390, 30), (690, 30)]

        for campo, posicion in zip(campos, posiciones):
            lbl_campo = Label(self.ventana, text=f'{campo} :', font=('Arial', 14), fg='white', bg=color_principal)
            lbl_campo.place(x=posicion[0], y=posicion[1])

    def entry_widgets(self):
        # Crear widgets de entrada (Entry) para diferentes campos.
        campos = ['nombre', 'materia', 'nota', 'jornada', 'estado']
        posiciones = [(150, 60), (150, 133), (450, 130), (450, 60), (720, 60)]

        # Diccionario para almacenar variables de tipo StringVar asociadas a cada campo.
        self.vars = {campo: StringVar() for campo in campos}

        # Crear el campo 'nombre' como Entry
        self.txtnombre = tk.Entry(self.ventana, font=('Arial', 12, 'normal'), textvariable=self.vars['nombre'],
                                  bd=1, relief='solid', fg='#5e617d', background='#FFFFFF')
        self.txtnombre.place(x=posiciones[0][0], y=posiciones[0][1])

        # Crear campos 'materia', 'nota', 'jornada', 'estado' como Entry
        for campo, posicion in zip(campos[1:], posiciones[1:]):
            entry_campo = Entry(self.ventana, font=('Arial', 12, 'normal'), textvariable=self.vars[campo],
                                bd=1, relief='solid', fg='#5e617d', background='#FFFFFF', validate='key',
                                validatecommand=(self.validate_nota, '%P'))
            entry_campo.place(x=posicion[0], y=posicion[1])

        # Campo de búsqueda
        self.buscar_var = StringVar()
        self.text_buscar = Entry(self.ventana, font=('Arial', 12), textvariable=self.buscar_var, bd=0, relief='solid',
                                 fg='#5e617d', background='#FFFFFF', highlightbackground='#7A7A7A')
        self.text_buscar.place(x=60, y=440)

        # Establecer el foco en el campo de entrada 'nombre'
        self.txtnombre.focus_set()

    def buttons(self):
        # Crear botones con etiquetas y comandos asociados.
        botones = [
            ("Guardar", 950, 440, self.guardar),
            ("Cancelar", 1050, 440, self.cancelar),
            ("Buscar", 250, 440, self.buscar)
        ]

        for texto, x, y, comando in botones:
            button = Button(self.ventana, text=texto, relief="flat", cursor="hand2", background=color_botones,
                            foreground=color_texto_botones, command=comando)
            button.place(x=x, y=y, width=90)
            button.bind("<Enter>", self.on_hover)
            button.bind("<Leave>", self.on_leave)

    def buscar(self):
        # Método para manejar la búsqueda de registros.
        if self.text_buscar:
            ref = self.text_buscar.get()
            self.limpiar_lista(ref)
            self.draw_list(ref)
        else:
            print("Error: self.text_buscar no está inicializado correctamente.")

    def guardar(self):
        # Método para manejar el guardado de registros.
        # Obtener valores de los Entry widgets
        arr = [self.vars[campo].get() for campo in ['nombre', 'materia', 'nota', 'jornada', 'estado']]

        # Verificar si los campos requeridos están vacíos
        campos_faltantes = [campo.capitalize() for campo, valor in zip(['nombre', 'materia', 'nota', 'jornada', 'estado'], arr) if valor == '']

        if campos_faltantes:
            campos_faltantes_str = ', '.join(campos_faltantes)
            mensaje = f"Por favor, complete los campos: {campos_faltantes_str}."
            messagebox.showwarning("Advertencia", mensaje)
            return

        # Validar la nota antes de guardar
        if not self.validate_nota(arr[2]):
            return

        # Confirmar antes de guardar
        confirmacion = messagebox.askquestion("Confirmar", "¿Estás seguro de que quieres guardar este estudiante?")

        if confirmacion == 'no':
            return

        # Si todos los campos requeridos están llenos y se confirma, proceder con el guardado
        d = Data()
        d.InsertItems(arr)

        # Limpiar los Entry widgets
        for campo in self.vars.values():
            campo.set("")

        # Actualizar la vista de la lista
        self.limpiar_lista()
        self.draw_list("")

        messagebox.showinfo("Guardado", "Los datos se han guardado exitosamente.")

    def cancelar(self):
        # Método para cancelar la entrada y limpiar los campos.
        for var in self.vars.values():
            var.set("")

    def limpiar_lista(self, ref=None):
        # Método para limpiar la lista de registros.
        if hasattr(self, 'lista'):
            self.lista.delete(*self.lista.get_children())

    def draw_list(self, ref):
        # Método para dibujar la lista de registros.
        self.lista = ttk.Treeview(self.ventana, columns=(1, 2, 3, 4, 5), show='headings', height='8')

        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('Treeview.Heading', background=color_botones, relief='flat', foreground='white')

        self.lista.heading(1, text='Nombre')
        self.lista.heading(2, text='Materia')
        self.lista.heading(3, text='Nota')
        self.lista.heading(4, text='Jornada')
        self.lista.heading(5, text='Estado')

        self.lista.heading(2, anchor=CENTER)

        self.lista.bind("<Double 1>", self.get_line)

        d = Data()
        if ref == "":
            elements = d.returnAllElements()
        else:
            elements = d.ReturnForSubject(ref)

        # Verificar si no hay elementos para mostrar y mostrar un mensaje en ese caso
        if not elements:
            messagebox.showinfo("Información", f"No hay registros para la materia: {ref}")
            return

        for i in elements:
            self.lista.insert('', 'end', values=i)

        self.lista.place(x=100, y=200)

    def get_line(self, event):
        # Método para manejar eventos de doble clic en la lista.
        item_selected = self.lista.selection()

        if item_selected:
            element = self.lista.item(item_selected, 'values')

            if element:
                n = element[0]
                m = element[1]
                na = StringVar(value=element[2])
                j = element[3]
                e = element[4]

                no = StringVar(value=n)
                ma = StringVar(value=m)
                jo = StringVar(value=j)
                es = StringVar(value=e)

                pop = Toplevel(self.ventana)
                pop.geometry("400x200")
                pop.resizable(False, False)
                pop.attributes('-toolwindow', 1)
                pop.configure(background="#dc5d6b")

                # Establecer las coordenadas para la esquina superior izquierda
                pop.geometry(f'+{self.ventana.winfo_x()}+{self.ventana.winfo_y()}')

                frame_top = Frame(pop, width=400, height=2, bg=color_bordes)
                frame_top.pack(side=tk.TOP, anchor=tk.N, fill=tk.X)

                frame_bottom = Frame(pop, width=400, height=2, bg=color_bordes)
                frame_bottom.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)

                frame_left = Frame(pop, width=2, height=180, bg=color_bordes)
                frame_left.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

                frame_right = Frame(pop, width=2, height=180, bg=color_bordes)
                frame_right.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y)

                txt_n = Entry(pop, textvariable=no, state="readonly", relief='flat').place(x=40, y=40)
                txt_m = Entry(pop, textvariable=ma, relief='flat').place(x=40, y=80)
                txt_na = Entry(pop, textvariable=na, relief='flat').place(x=40, y=120)
                txt_j = Entry(pop, textvariable=jo, relief='flat').place(x=199, y=40)
                txt_e = Entry(pop, textvariable=es, relief='flat').place(x=199, y=80)

                btn_Modificar = Button(pop, text="Actualizar", relief="flat", background=color_bordes, foreground="white",
                                       cursor="hand2", command=lambda: self.edit(n, ma.get(), na.get(), jo.get(), es.get(), item_selected, pop))
                btn_Modificar.place(x=180, y=120, width=90)

                btn_Eliminar = Button(pop, text="Eliminar", relief="flat", background=color_bordes, foreground="white",
                                      cursor="hand2", command=lambda: self.delete(no.get(), pop)).place(x=290, y=120, width=90)

    def edit(self, n, m, na, j, e, item_selected, pop):
            # Crear una instancia de la clase Data (asumiendo que existe) para realizar operaciones en la base de datos
        d = Data()

        # Crear una lista con los valores actualizados para el estudiante
        arr = [n, m, na, j, e]

        # Validar la nota antes de realizar la actualización en la base de datos
        if not self.validate_nota(na):
            return

        # Llamar al método UpdateItem de la clase Data para actualizar los datos del estudiante en la base de datos
        d.UpdateItem(arr, n)

        # Mostrar un mensaje de información sobre la actualización exitosa
        messagebox.showinfo("Actualización", f"Se ha actualizado correctamente a {n}")

        # Limpiar la lista y volver a dibujarla para reflejar los cambios
        self.limpiar_lista()
        self.draw_list("")

        # Cerrar la ventana emergente después de completar la actualización
        pop.destroy()

    def delete(self, n, pop):
        try:
            # Crear una instancia de la clase Data (asumiendo que existe) para realizar operaciones en la base de datos
            d = Data()

            # Llamar al método Delete de la clase Data para eliminar al estudiante de la base de datos
            d.Delete(n)

            # Mostrar un mensaje de información sobre la eliminación exitosa
            messagebox.showinfo("Eliminación", f"Se ha eliminado correctamente a {n}")

            # Limpiar la lista y volver a dibujarla para reflejar los cambios
            self.limpiar_lista()
            self.draw_list("")
        except Exception as e:
            # Mostrar un mensaje de error si ocurre alguna excepción durante la eliminación
            messagebox.showerror(title="Error", message=f"Error al eliminar: {str(e)}")
            return

        # Cerrar la ventana emergente después de mostrar el mensaje de información
        pop.destroy()

    def validate_nota(self, value):
        try:
            print("Validating...")

            # Verificar si el campo de nota está vacío y considerarlo válido
            if not value:
                return True

            # Convertir el valor a tipo float para realizar la validación
            nota = float(value)

            # Verificar si la nota está en el rango permitido (0.0 a 5.0)
            if 0.0 <= nota <= 5.0:
                return True
            else:
                # Mostrar una advertencia si la nota está fuera del rango permitido
                messagebox.showwarning("Advertencia", "La nota debe estar en el rango de 0.0 a 5.0")
                return False
        except ValueError:
            # Mostrar una advertencia si el valor no se puede convertir a tipo float
            messagebox.showwarning("Advertencia", "Por favor, ingrese un valor numérico válido para la nota.")
            return False

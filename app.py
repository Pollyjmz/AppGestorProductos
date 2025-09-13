from tkinter import *
from tkinter import ttk
from db import Session, Producto

class VentanaPrincipal:
    def __init__(self, root):
        self.ventana = root
        self.session = Session()
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(width=True, height= True)
        self.ventana.wm_iconbitmap(r"Resources\logo.ico")

        #Frame principal
        frame = LabelFrame(self.ventana, text= "registrar un producto nuevo")
        frame.grid ( row=0,column=0, columnspan=3, pady = 20)
        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")  # Etiqueta de texto ubicada en ele
        self.etiqueta_nombre.grid(row=1, column=0)  # Posicionamiento a traves de grid
        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.nombre.focus()  # Para que el foco del raton vaya a este Entry al inicio
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio (caja de texto que recibira el precio)
        self.precio = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.precio.grid(row=2, column=1)

        # Boton Guardar Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command= self.add_producto)
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W + E)

        #  Label para mostrar mensajes de validación
        self.mensaje = Label(self.ventana, text="", fg="red")
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',                                                          11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",font=('Calibri', 13, 'bold')) # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes
         # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, 'bold'))
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=5, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR',command =self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=5, column=1, sticky=W + E)

        self.get_productos()



    def get_productos(self):
        registros_tabla = self.tabla.get_children()  # Obtener todos los datos de la  tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        session =  Session()
        registros = session.query(Producto).order_by(Producto.nombre.desc()).all()
        session.close()

        for registro in registros:
            self.tabla.insert("", 0, text=registro.nombre, values=(registro.precio,))

    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False


    def add_producto(self):
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacío'

            return
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un número válido mayor que 0'

            return

        session = Session()
        nuevo = Producto(nombre=self.nombre.get(), precio=float(self.precio.get()))
        session.add(nuevo)
        session.commit()
        session.close()

        self.mensaje['text'] = "Producto guardado con éxito"
        self.nombre.delete(0, END)
        self.precio.delete(0, END)
        # Debug
        # print(self.nombre.get())
        # print(self.precio.get())
        self.get_productos()


    def del_producto(self):
        try:
         nombre = self.tabla.item(self.tabla.selection())['text']
        except IndexError:
         self.mensaje['text'] = 'Por favor, seleccione un producto'
         return

        session = Session()
        producto = session.query(Producto).filter_by(nombre=nombre).first()
        if producto:
            session.delete(producto)
            session.commit()
            self.mensaje['text'] = f'Producto {nombre} eliminado con éxito'
        else:
            self.mensaje['text'] = f'Producto {nombre} no encontrado'
        session.close()
        self.get_productos()


    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'


class VentanaEditarProducto():
    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri',13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar,value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1,column=1)
        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri',13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri',13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3,column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri',13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Botón Actualizar Producto
        ttk.Style().configure('my.TButton', font=('Calibri', 14, 'bold'))

        # Ejemplo de cómo creamos y configuramos el estilo en una sola línea
        ttk.Button(frame_ep, text="Actualizar Producto",style='my.TButton', command=self.actualizar).grid(row=5, columnspan=2, sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio

        session = Session()
        producto = session.query(Producto).filter_by(nombre=self.nombre).first()
        if producto:
            producto.nombre = nuevo_nombre
            producto.precio = float(nuevo_precio)
            session.commit()
            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.mensaje['text'] = f'No se encontró el producto {self.nombre}'
        session.close()
        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()



if __name__ == "__main__":
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()  # tiene que ser la ultima



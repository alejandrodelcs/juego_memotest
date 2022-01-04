from tkinter import *
from tkinter import messagebox
from memotest import memotest
from random import shuffle
import os.path as path
from tkinter import ttk
import string
import re

DEFAULT = 9999
MAX_JUGADORES_PERMITIDOS = 1


# ------------------------------------------- Clase inicio ------------------------------------------------------------ #

class inicio(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry("1600x800")
        self.master.configure(bg="MediumPurple4")
        self.master.attributes('-alpha', 0.9)
        self.master.title("Memotest")
        self.master.iconbitmap("images\\abc.ico")
        self.master.resizable(False, False)
        self.logueados = []
        self.configuracion = self.leerConfiguracion()
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.crearWidgetIngreso()

    """
        PRE: Abre el archivo configuracion.csv
        POST: retorna una lista con datos de la configuracion
    """

    def leerConfiguracion(self):
        listaConfiguracion = []
        with open("configuracion.csv", "r") as config:
            lineaConfiguracion = config.readline().rstrip('\n').split(',')
            while lineaConfiguracion != ['']:
                listaConfiguracion.append(lineaConfiguracion[1])
                lineaConfiguracion = config.readline().rstrip('\n').split(',')
        return listaConfiguracion

    """
        PRE: Crea la ventana de Inicio
        POST:
    """

    def crearWidgetIngreso(self):

        self.frameIngreso = Frame(self.master, bg="MediumPurple4")
        self.frameIngreso.grid(row=0, column=0, pady=100, padx=600)

        self.treeviewIngreso = ttk.Treeview(
            self.frameIngreso, columns='Nombre')
        self.treeviewIngreso.grid(row=0, column=0)
        self.style.configure("Treeview.Heading", font=(None, 10))

        self.entryFrame = Frame(self.master, bg="MediumPurple4")
        self.entryFrame.grid(row=1, column=0, pady=5, padx=300)

        self.buttonFrame = Frame(self.master, bg="MediumPurple4")
        self.buttonFrame.grid(row=2, column=0, pady=5, padx=0)

        self.treeviewIngreso.column('#0', width=0, stretch=NO)
        self.treeviewIngreso.heading('#0', text="", anchor=W)

        self.treeviewIngreso.column(
            'Nombre', anchor=CENTER, width=320, stretch=NO)
        self.treeviewIngreso.heading('Nombre', text='Nombre', anchor=CENTER)

        Label(self.entryFrame, text="Usuario", bg="MediumPurple4",
              fg="white", font="Arial 12 bold").grid(row=0, column=0)
        self.entryUsuario = Entry(self.entryFrame, font="Arial 13")
        self.entryUsuario.grid(row=1, column=0, ipady=3, ipadx=20)

        Label(self.entryFrame, text="Contraseña", bg="MediumPurple4",
              fg="white", font="Arial 12 bold").grid(row=0, column=1)
        self.entryPass = Entry(self.entryFrame, show='*', font="Arial 13")
        self.entryPass.grid(row=1, column=1, ipady=3,
                            ipadx=20, pady=20, padx=90)

        Label(self.master, text=f"Usuarios Permitidos: {self.configuracion[MAX_JUGADORES_PERMITIDOS]}",
              font=("Arial", 13), fg="white", bg='MediumPurple4').place(x=100, y=720)

        self.buttonIngresar = Button(self.buttonFrame, text="Ingresar",
                                     width=9, font="Arial 15", bg="black", fg="white", command=self.nuevaVentanaLogin)
        self.buttonIngresar.grid(row=1, column=0, pady=30)
        self.buttonRegistrar = Button(self.buttonFrame, text="Registrar",
                                      width=9, font="Arial 15", bg="black", fg="white", command=self.nuevaVentanaRegistrar)
        self.buttonRegistrar.grid(row=1, column=1, pady=30, padx=30)
        self.iniciar_tbn = PhotoImage(file="images\\play_btn_3.png")
        self.buttonPlay = Button(self.buttonFrame, image=self.iniciar_tbn, borderwidth=0,
                                 bg="MediumPurple4", activebackground="MediumPurple4", command=self.nuevaVentanaMemotest)
        self.buttonPlay.grid(row=1, column=2, padx=40)

    """
        PRE: El usuario tiene que estar en usuarios.csv para ser insertado en el treeview y poder ingresar al juego
        POST:
    """

    def nuevaVentanaLogin(self):
        self.appLogin = login(self.master)
        usuario = self.entryUsuario.get()
        clave = self.entryPass.get()
        loginValido = self.appLogin.ingresarSistema(usuario, clave)

        if usuario not in self.logueados:
            if loginValido:
                self.entryUsuario.delete(0, END)
                self.entryPass.delete(0, END)
                self.logueados.append(usuario)
                self.treeviewIngreso.insert('', 'end', values=usuario)
        else:
            messagebox.showerror("Error", "el usuario ya fue ingresado")

        if len(self.logueados) == int(self.configuracion[MAX_JUGADORES_PERMITIDOS]):
            messagebox.showinfo(
                "Importante", "Alcanzó el máximo de usuarios permitidos\n\tEmpieza el Juego")
            self.nuevaVentanaMemotest()

    """
        PRE: Abre la ventana del Registro
        POST: 
    """

    def nuevaVentanaRegistrar(self):
        self.entryUsuario.delete(0, END)
        self.entryPass.delete(0, END)
        self.appRegistro = login(self.master)
        self.appRegistro.registrar()

    """
        PRE: Abre la ventana la ventana del juego memotest siempre y cuando no alcanze el maximo permitido de
            jugadores o exista usuarios ingresados de manera exitosa en Inicio.
        POST: -
    """

    def nuevaVentanaMemotest(self):

        if len(self.logueados) > 0:
            self.frameIngreso.destroy()
            self.entryFrame.destroy()
            self.treeviewIngreso.destroy()
            self.buttonFrame.destroy()
            self.appNivel = nivel(
                self.master, self.logueados, self.configuracion[2], self.configuracion[1])
        else:
            messagebox.showerror("Error", "No hay usuarios registrados")


# ---------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------- Clase nivel---------------------------------------------------------- #


class nivel(Frame):
    """
        PRE: El constructor recibe una lista con los usuarios aceptados, la maxima cantidad de partidas
            y la cantidad maxima de jugadores.
        POST:
    """

    def __init__(self, master, jugadores, partidasMax, jugadoresMax):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Nivel")
        self.jugadores = len(jugadores)
        self.listaJugadores = jugadores
        self.partidasMax = partidasMax
        self.jugadoresMax = jugadoresMax
        self.reinicio = StringVar()
        self.opcion = IntVar()
        self.crearWidgetNivel()

    """
    PRE     Recibe el nivel de dificultad.
    POST:   Si la dificultad seleccionada es valida, se construye el archivo "configuracion.csv" con
            la cantidad de fichas, cantidad de jugadores, cantidad de partidas y si se desea
            reiniciar el archivo de partidas.
    Julian Montenegro, Agustin Allelo
    """

    def ingresar(self):
        opciones = [2, 4, 8]

        if self.opcion.get() in opciones:

            config = open("configuracion.csv", "w")
            config.write("CANTIDAD_FICHAS," + str(self.opcion.get()) + "\n")
            config.write("MAXIMO_JUGADORES," + str(self.jugadoresMax) + "\n")
            config.write("MAXIMO_PARTIDAS," + str(self.partidasMax) + "\n")
            config.write("REINICIAR_ARCHIVO_PARTIDAS," +
                         self.reinicio.get() + "\n")
            config.close()
            reinicioInfo = "Si" if self.reinicio.get() == "True" else "No"
            messagebox.showinfo(
                "Importante", f"Cantidad de Fichas: {str(self.opcion.get())}\nCantidad de Jugadores: {self.jugadores}\nCantidad de Partidas (Maximas):{self.partidasMax}\nReinicio: {reinicioInfo}\n")
            self.frameNivel.destroy()
            shuffle(self.listaJugadores)
            self.appMemotest = memotest(self.master, self.listaJugadores)

        else:
            messagebox.showerror(
                "Nivel", "¡Error! Usted no selecciono ningun nivel")

    """
    PRE     Recibe la opcion de dificultad deseada con el self.opcion.get().
    POST:   Retorna el nivel de dificultad.
    Julian Montenegro, Agustin Allelo
    """

    """
        PRE: Crea la ventana donde el usuario puede elegir el Nivel y si desea Reiniciar las partidas
        POST: 
    """

    def crearWidgetNivel(self):

        self.frameNivel = Frame(self.master, bg="MediumPurple4")
        self.frameNivel.place(relx=0.45, rely=0.15)

        self.heading = Label(self.frameNivel, text="Nivel", font='Arial 35 bold', fg='thistle1',
                             bg='MediumPurple4').grid(row=1, column=1, pady=25, sticky='w')

        self.facil = Radiobutton(self.frameNivel, text="Facil", variable=self.opcion, value=2, font='Arial 11',
                                 bg='MediumPurple4', fg='pale turquoise', selectcolor="MediumPurple4")
        self.facil.grid(row=2, column=1, pady=25, sticky='w')
        self.medio = Radiobutton(self.frameNivel, text="Medio", variable=self.opcion, value=4, font='Arial 11',
                                 bg='MediumPurple4', fg='pale turquoise', selectcolor="MediumPurple4")
        self.medio.grid(row=3, column=1, pady=25, sticky='w')
        self.dificil = Radiobutton(self.frameNivel, text="Dificil", variable=self.opcion, value=8, font='Arial 11',
                                   bg='MediumPurple4', fg='pale turquoise', selectcolor="MediumPurple4")
        self.dificil.grid(row=4, column=1, pady=25, sticky='w')
        self.reinicioCheckbutton = Checkbutton(self.frameNivel, text="Reinicio *", variable=self.reinicio, onvalue="True", offvalue="False", font='Arial 11',
                                               bg='MediumPurple4', fg='pale turquoise', selectcolor="MediumPurple4")
        self.reinicioCheckbutton.deselect()
        self.reinicioCheckbutton.grid(row=5, column=1, pady=30, sticky='w')
        Label(self.master, text="* Si marca la opción de Reinicio las partidas se borrara al empezar nuevamente el juego",
              font=("Arial", 10), fg="white", bg='MediumPurple4').place(x=100, y=720)

        self.iniciar_tbn = PhotoImage(file="images\\play_btn_3.png")
        self.buttonPlay = Button(self.frameNivel, image=self.iniciar_tbn, borderwidth=0,
                                 bg="MediumPurple4", activebackground="MediumPurple4", command=self.ingresar)
        self.buttonPlay.grid(row=6, column=1)


# ---------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------- Clase Login---------------------------------------------------------- #


class login(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.logueados = []

    @staticmethod
    def ingresoVacio(usuario, clave):
        return usuario or clave

    @staticmethod
    def hayDatosEnArchivo(linea):
        return linea

    """
    PRE     Recibe el nombre de usuario a registrar con la variable user.
    POST:   Retorna True si el nombre de usuario es valido para registrar.
    Julian Montenegro, Agustin Allelo
    """
    @staticmethod
    def validarUser(user):
        permitido = string.ascii_lowercase+string.ascii_uppercase+'1234567890-_áéíóúÁÉÍÓÚ'
        pos = 0
        contador = 0
        hayGuionBajo = '_' in user
        if len(user) > 3 and len(user) < 16 and hayGuionBajo and bool(re.search(r'\d', user)):
            while pos < len(user) and pos != -1:
                if user[pos] not in permitido:
                    pos = -2
                elif user[pos].isalpha():
                    contador += 1
                pos += 1
        return pos > 0 and contador > 0

    """
    PRE     Recibe la contraseña a registrar con la variable password.
    POST:   Retorna True si la contraseña es valida para registrar.
    Julian Montenegro, Agustin Allelo
    """
    @staticmethod
    def validarPassword(password):
        permitido = string.ascii_lowercase+string.ascii_uppercase+'1234567890-_'
        pos = 0
        contador = 0
        tamanioPermitido = len(password) > 7 and len(
            password) < 13
        estaEnMayuscula = password.isupper()
        estaEnMinuscula = password.islower()
        if '_' in password or '-' in password:
            while pos < len(password) and pos != -1:
                if password[pos] not in permitido:
                    pos = -2
                elif password[pos].isalpha():
                    contador += 1
                pos += 1
        return tamanioPermitido and not estaEnMayuscula and not estaEnMinuscula and bool(re.search(r'\d', password)) and contador > 0 and pos > 0

    def leerArchivo(self, archivo):
        datos = archivo.readline()
        return datos.rstrip("\n").split(",") if datos else [DEFAULT, ""]

    """
    PRE     Recibe el usuario y la contraseña a logear con las variables usuario
            y clave
    POST:   Valida si se encuentran en el archivo y al logear todos los jugadores inicia el juego
    Julian Montenegro, Agustin Allelo
    """

    def ingresarSistema(self, usuario, clave):
        encontrado = False
        valido = False
        if path.exists("usuarios.csv"):
            if self.ingresoVacio(usuario, clave):
                with open("usuarios.csv", "r") as usuarios:
                    usuarios.seek(0)
                    lineaUsuario = self.leerArchivo(usuarios)
                    if lineaUsuario:
                        while lineaUsuario[0] != DEFAULT and lineaUsuario[0] != usuario and not encontrado:
                            lineaUsuario = self.leerArchivo(usuarios)
                        lineaIngreso = [usuario, clave]
                        if lineaUsuario == lineaIngreso and usuario not in self.logueados:
                            encontrado = True
                            self.logueados.append(lineaUsuario[0])
                            messagebox.showinfo("Login", "¡Ingreso Correcto!")
                            valido = True
                            usuarios.seek(0)
                        else:
                            usuarios.seek(0)
                            messagebox.showerror(
                                "Login", "Usuario Inexistente o hay error en alguno de los campos \nIntentelo nuevamente o registrese")
                    else:
                        messagebox.showerror(
                            "Login", "No se encontro datos en el sistema\n\tRegistrese")
                        usuarios.seek(0)
            else:
                messagebox.showinfo(
                    "Login", "Los datos ingresados se encuentra vacios")
        else:
            messagebox.showerror(
                "Login", "No se encontro datos en el sistema\n\tRegistrese")

        return valido

    def guardarDatosUsuarios(self):
        if not path.exists("usuarios.csv"):
            usuarios = open("usuarios.csv", "w")
            usuarios.close()

        linea = self.user.get() + "," + self.password.get()
        user = self.user.get()
        with open("usuarios.csv", "r+") as usuarios:
            if linea != ",":
                validacionUsuario = self.validarUser(self.user.get())
                validacionClave = self.validarPassword(self.password.get())
                if validacionUsuario and validacionClave:
                    if self.password.get() == self.passwordValidate.get():
                        lineaUsuarios = self.leerArchivo(usuarios)
                        while lineaUsuarios[0] != DEFAULT and lineaUsuarios[0] != user:
                            lineaUsuarios = self.leerArchivo(usuarios)
                        if lineaUsuarios[0] == user:
                            messagebox.showerror(
                                "Usuarios", "¡Error!El nombre de usuario ya está en uso.")
                        else:
                            usuarios.write(linea + "\n")
                            messagebox.showinfo(
                                "Usuarios", "¡Usuario registrado con exito!")

                            self.frameRegister.destroy()
                    else:
                        messagebox.showerror(
                            "Usuarios", "Las contraseñas no coinciden\nVuelva a intentarlo")
                else:
                    messagebox.showerror(
                        "Usuarios", "El dato ingresado no cumple con los requisitos de longitud y complejidad\nVuelva a intentarlo")
            else:
                messagebox.showenfo("Usuarios", "No Ingreso Datos")
            usuarios.seek(0)

    def cerrarVentana(self):
        self.frameRegister.destroy()

    """  
    PRE:   Construye un Frame de tkinter con todos los elementos necesarios 
            para el registro de los jugadores.
    POST: -
    Julian Montenegro, Agustin Allelo
    """

    def registrar(self):
        self.frameRegister = Toplevel(
            self.master, bg='LavenderBlush3', pady=20)
        self.frameRegister.geometry('440x425')
        self.frameRegister.resizable(width=False, height=False)
        self.frameRegister.title("Registrar")
        self.frameRegister.iconbitmap('images\\registration.ico')
        text = ['Usuario',
                'Contraseña', 'Vuelve a escribir\n la contraseña']

        self.frameButtonRegistro = Frame(
            self.frameRegister, bg='LavenderBlush3')
        self.frameButtonRegistro.grid(row=6, column=1, pady=50)

        self.heading = Label(self.frameRegister, text="Registrar",
                             font='Verdana 20 bold', fg="DodgerBlue4", bg='LavenderBlush3').grid(row=0, column=1, pady=20)

        for i in range(len(text)):
            if text[i] != 'Contraseña' or text[i] != 'Vuelve a escribir \nla contraseña':
                Label(self.frameRegister, text=text[i], font=("Arial", 10), fg="black", bg='LavenderBlush3').grid(
                    row=i+3, column=0, sticky='e', padx=10, pady=10)
            else:
                Label(self.frameRegister, text=text[i], font=("Arial", 10), fg="black", bg='LavenderBlush3').grid(
                    row=i+3, column=0, sticky='e', padx=10, pady=10).config(show="*")

        self.user = Entry(self.frameRegister)
        self.user.grid(row=3, column=1, padx=10, pady=28, ipadx=40)

        self.password = Entry(self.frameRegister)
        self.password.grid(row=4, column=1, padx=10, pady=28, ipadx=40)
        self.password.config(show="*")

        self.passwordValidate = Entry(self.frameRegister)
        self.passwordValidate.grid(row=5, column=1, padx=10, pady=10, ipadx=40)
        self.passwordValidate.config(show="*")

        Label(self.frameRegister, text="Debe contar con 4 o 15 caracteres alfanumericos, ",
              font=("Arial", 8), fg="red3", bg='LavenderBlush3').place(x=128, y=130)
        Label(self.frameRegister, text="letras,números y guión bajo ( _ ) ",
              font=("Arial", 8), fg="red3", bg='LavenderBlush3').place(x=128, y=145)

        Label(self.frameRegister, text="Debe contar con 8 o 12 caracteres alfanumericos.",
              font=("Arial", 8), fg="red3", bg='LavenderBlush3').place(x=128, y=200)
        Label(self.frameRegister, text="Al menos un “ _ ” o “ - “ y no letras acentuadas ",
              font=("Arial", 8), fg="red3", bg='LavenderBlush3').place(x=128, y=220)

        self.buttonGuardarDatos = Button(self.frameButtonRegistro,
                                         width=9,
                                         text='Registrar',
                                         command=self.guardarDatosUsuarios, font=("Arial", 10), fg="black", bg="silver")
        self.buttonGuardarDatos.grid(row=0, column=0, padx=10)

        self.buttonCancelar = Button(self.frameButtonRegistro,
                                     width=9,
                                     text='Cancelar',
                                     command=self.cerrarVentana, font=("Arial", 10), fg="black", bg="silver")
        self.buttonCancelar.grid(row=0, column=1)


# ------------------------------------------------------------------------------------------------------------------------- #

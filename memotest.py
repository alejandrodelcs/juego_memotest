from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from modulos import *
from datetime import datetime
from os import remove, rename
import os.path as path
from time import strftime


MAX_TURNOS = 2
POS_FICHAS = 0
MAX = 9999


# ---------------------------------------------- Clase Memotest ---------------------------------------------------------- #

class memotest(Frame):
    """
        PRE: El constructor recibe la raiz de Tk, inicializa las posiciones,
            y una lista con el nombre de los usuarios aceptados (jugador)
        POST: -
        Alejandro Del Carpio
    """

    def __init__(self, master, listaUsuarios):
        Frame.__init__(self, master)
        self.master = master
        self.configuracion = self.leerConfiguracion()
        tamanio = self.cambiarTamanioVentana(self.configuracion)
        self.master.configure(background="gray20")
        self.master.resizable(width=False, height=False)
        self.master.title("Memotest")
        self.master.iconbitmap("images\\hojadedatos.ico")
        self.master.geometry(tamanio)
        self.startTime = None
        self.tablero = crearTablero(int(self.configuracion[0]))
        self.tableroPosiciones = crearPosiciones(int(self.configuracion[0]))
        self.diccUsuarios = crearDiccionario(listaUsuarios)
        self.punto = 0
        self.turno = 0
        self.ts = "00:00:00"
        self.crearWidgets()

    """
        PRE: Abre la ventana de resultados y destruye el Frame de Memotest 
        POST: -
        Alejandro Del Carpio
    """
    def nuevaVentanaTreeview(self):
        self.frameJuego.destroy()
        self.frameJugador.destroy()
        self.appTreeview = resultado(
            self.master, self.diccUsuarios, self.configuracion, self.ts)

    """
        PRE:  segun la configuracion establecida de dificultad/nivel, adaptara la resolucion de la ventana para el juego
        POST: -
        Alejandro Del Carpio
    """

    def cambiarTamanioVentana(self, configuracion):
        if int(configuracion[POS_FICHAS]) == 2:
            tamanio = "500x250"
        elif int(configuracion[POS_FICHAS]) == 4:
            tamanio = "500x400"
        else:
            tamanio = "500x700"
        return tamanio

    """
        PRE:  Lee el archivo configuracion.csv 
        POST: Retorna una lista con los datos del archivo configuracion.csv
        Alejandro Del Carpio
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
        PRE:  Inicia el Tiempo
        POST: -
        Alejandro Del Carpio
    """

    def updateTimer(self):
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            self.ts = str(delta).split('.')[0]  # drop ms
            if delta.total_seconds() < 36000:
                self.ts = "0" + self.ts  # zero-pad
        self.labelTiempo.config(text=self.ts)
        self.frameJugador.after(100, self.updateTimer)

    """
        PRE: Asigna los puntos a cada jugador 
        POST
        Alejandro Del Carpio
    """

    def puntaje(self):
        if self.punto == 0:
            self.usuarios[1] += 1
        else:
            self.usuarios[0] += 1
            self.usuarios[1] += 1
        self.turno += 1
        if self.turno == len(self.diccUsuarios):
            self.turno = 0

    """
        PRE:  Recibe la clase tkinter.button
        POST: -
        Alejandro Del Carpio
    """

    def refrescar(self):
        if self.punto == 0:
            messagebox.showerror("Advertencia", "¡Has fallado!")
            self.botones[0]["background"] = "cornflower blue"
            self.botones[0]["text"] = '?'
            self.botones[1]["background"] = "cornflower blue"
            self.botones[1]["text"] = '?'
        else:
            self.botones[0]["state"] = DISABLED
            self.botones[1]["state"] = DISABLED
            messagebox.showinfo("Felicidades", "¡Has acertado la letra!")
        self.coordenada = []
        self.botones = []
        self.usuarios = self.diccUsuarios[self.listaUsuarios[self.turno]]
        self.jugador["text"] = self.listaUsuarios[self.turno]

        if len(self.tableroPosiciones) == 0:
            self.startTime = None
            self.labelTiempo.config(text=self.ts)
            messagebox.showinfo("Mensaje", "JUEGO FINALIZADO")
            self.nuevaVentanaTreeview()
    """
        PRE:  Recibe la informacion de los botones en pantalla
        POST: -
    """

    def click(self, button):
        if self.startTime == None:
            self.startTime = datetime.now()

        if button["text"] == '?':
            self.info = button.grid_info()
            posicionX = self.info['row']
            posicionY = self.info['column']
            buscar_letra = dict(filter(
                lambda x: [posicionX, posicionY] in x[1], self.tableroPosiciones.items()))
            button.configure(text=(list(buscar_letra.keys()))
                             [0], background='chocolate2')
            self.coordenada.append([posicionX, posicionY])
            self.botones.append(button)

        if len(self.coordenada) == MAX_TURNOS:
            self.punto = comprobarLetra(
                self.tableroPosiciones, self.coordenada)
            self.puntaje()
            self.refrescar()

    """
        PRE: Crea la ventana del juego
        POST: -
    """

    def crearWidgets(self):
        self.frameJuego = Frame(self.master, width=400,
                                height=400, background="gray20")
        self.frameJuego.grid(row=2, column=0, padx=2, pady=5)

        self.frameJugador = Frame(self.master, background="gray20")
        self.frameJugador.grid(row=1, column=0)

        self.listaUsuarios = [usuario for usuario in self.diccUsuarios]
        self.usuarios = self.diccUsuarios[self.listaUsuarios[self.turno]]

        self.labelTiempo = Label(
            self.frameJugador, text="00:00:00", font='Arial 12', background="gray20", foreground="snow")
        self.labelTiempo.grid(row=1, column=0, pady=3)

        self.jugador = Label(
            self.frameJugador, text=self.listaUsuarios[self.turno], font="Arial 15 bold", background="gray20", foreground="snow")
        self.jugador.grid(row=0, column=0, pady=3)

        self.updateTimer()

        self.coordenada = []
        self.botones = []
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                self.tablero[i][j] = Button(self.frameJuego, text='?', font="Arial 13 bold", relief=SUNKEN,
                                            background="cornflower blue", command=lambda i=i, j=j: self.click(self.tablero[i][j]))
                self.tablero[i][j].grid(
                    row=i, column=j, padx=30, pady=30, ipadx=20, ipady=30)


# ----------------------------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------Clase Resultados ----------------------------------------------------------------------- #

class resultado(Frame):
    def __init__(self, master, diccUsuarios, listaConfiguracion, tiempo):
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry("1300x200")
        self.master.resizable(0, 0)
        self.master.title("Resultados")
        self.tiempo = tiempo
        self.partidas = 0
        self.jugadores = list(diccUsuarios.keys())
        self.scoreItems = list(diccUsuarios.items())
        self.MaxPartidas = listaConfiguracion[2]
        self.partidas = self.leerUltimaPartida()
        self.reiniciarJuego(listaConfiguracion[3])
        self.create_widgets()
        self.create_imagen()
        self.create_button()
        self.resultados()
    
    """
        PRE: Lee el archivo que contiene el número de partida
        POST:
    """
    def leerUltimaPartida(self):
        numeroPartida = 0
        if path.exists("ultimaPartida.txt"):
            partidaJugada = open("ultimaPartida.txt", 'r')
            numeroPartida = int(partidaJugada.read())
        return numeroPartida

    """
        PRE: Abre el juego memotest, crea un archivo .txt que alojara el número
            de partida, este se ira actualizando a medida que decida volver a 
            a jugar
        POST:
    """
    def nuevaVentanaMemotest(self):
        ultimaPartida = open("ultimaPartida.txt", 'w')
        self.partidas += 1
        ultimaPartida.write(str(self.partidas) + '\n')
        ultimaPartida.close()
        print(self.partidas)
        self.frame.destroy()
        self.treeview.destroy()

        self.appMemotest = memotest(self.master, self.jugadores)

    """
        PRE: Crea el treeview, junto con el frame y la scrollbar
        POST:
        Leandro.A.Peñaloza
    """

    def create_widgets(self):
        self.frame = Frame(self.master)
        self.frame.place(relx=.8, relwidt=0.2, relheight=1)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.treeview = ttk.Treeview(self.master, yscrollcommand=self.scrollbar.set, columns=(
            "col1", "col2", "col3", "col4"))

        color = 'gray1'
        self.treeview.tag_configure(color, background='#444444')
        self.treeview.tag_configure(
            'fuente', font=("Arial", 10), foreground='gold1')

        self.scrollbar.config(command=self.treeview.yview)
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        self.treeview.heading("#0", text="Fecha", anchor=CENTER)
        self.treeview.heading("col1", text="Tiempo", anchor=CENTER)
        self.treeview.heading("col2", text="Jugador", anchor=CENTER)
        self.treeview.heading("col3", text="Aciertos", anchor=CENTER)
        self.treeview.heading("col4", text="Intentos", anchor=CENTER)

        self.treeview.place(relwidt=.8, relheight=1)

    """
        PRE: Cierra el treeview con los resultados obtenidos en el juego
        POST:
    """   
    def salirJuego(self):
        if path.exists("ultimaPartida.txt"):
            remove("ultimaPartida.txt")
        self.master.destroy()

    """
        PRE: Se pasa un string que representa True/False. True vuelve a
            generar el archivo partidasA.csv 
        POST:
    """
    def reiniciarJuego(self,reinicio):
        if reinicio == "True":
            self.RankingA = open("partidasA.csv", "w")
            self.RankingA.close()


    """
        PRE: Crea los botones "Volver a jugar" y "Resumen"
        POST:
        Leandro.A.Peñaloza
    """

    def create_button(self):
        self.boton = Button(self.frame, text="Volver a jugar",
                            bg="snow", command=self.nuevaVentanaMemotest)
        self.boton2 = Button(self.frame, text="Resumen",
                             bg="snow", command=self.resumen)
        self.boton.place(relx=.30, rely=.3, relwidt=.5, relheight=.1)
        self.boton2.place(relx=.30, rely=.5, relwidt=.5, relheight=.1)
        self.boton3 = Button(self.frame, text="Salir",
                             bg="snow", command=self.salirJuego)
        self.boton3.place(relx=.30, rely=.7, relwidt=.5, relheight=.1)

    """
        PRE: Crea un label para contener la imagen del resultado
        POST:
        Leandro.A.Peñaloza
    """

    def create_imagen(self):
        self.wallpaperResultados = PhotoImage(
            file="images\FondoResultados2.png")
        Label(self.frame, image=self.wallpaperResultados).place(x=15, y=7)

    """
        PRE: Muestra los resultados insertandolos en el treeview y llamar a Archivos
        POST:
        Leandro.A.Peñaloza
    """

    def resultados(self):
        self.scoreItems.sort(key=lambda x: x[1][1])
        self.scoreItems.sort(key=lambda x: x[1][0], reverse=True)
        self.tiempo
        self.fecha = str(strftime("%d/%m/%y"))
        self.Archivos()

        if self.partidas == int(self.MaxPartidas):
            if path.exists("ultimaPartida.txt"):
                remove("ultimaPartida.txt")
            messagebox.showinfo(
                "Importante", "Se alcanzo el máximo de partidas")
            self.boton["state"] = DISABLED
        
        for i in range(0, len(self.scoreItems)):
            self.lineaResultadoJuego = self.fecha + ',' + str(self.tiempo) + ',' + str(self.scoreItems[i][0]) + ',' + str(
                self.scoreItems[i][1][0]) + ',' + str(self.scoreItems[i][1][1])
            self.treeview.insert("", END, text=self.fecha, values=[
                                 self.tiempo, self.scoreItems[i][0], self.scoreItems[i][1][0], self.scoreItems[i][1][1]])
        self.treeview.item('I001', tag=('fuente', 'gray1'))

    """
        PRE: Recibe el diccionario con los puntajes y lee los archivos, ordenandolo de forma descendiente
        POST:
        Leandro.A.Peñaloza
    """

    def Archivos(self):
        if not path.exists("partidasA.csv") and not path.exists("partidasB.csv"):
            self.RankingA = open("partidasA.csv", "w")
            i = 0  # Utilizada para moverme atraves del diccionario.
            while i < len(self.scoreItems):
                linea = self.fecha + ',' + str(self.tiempo) + ',' + str(self.scoreItems[i][0]) + ',' + str(
                    self.scoreItems[i][1][0]) + ',' + str(self.scoreItems[i][1][1]) + "\n"
                self.RankingA.write(linea)
                i += 1
            self.RankingA.close()
        elif path.exists("partidasA.csv") and not path.exists("partidasB.csv"):
            self.RankingA = open("partidasA.csv", "r")
            self.RankingB = open("partidasB.csv", "w")
            # Resultado esta formado por Fecha, Tiempo, Usuario, Puntaje, Intentos (EJ: Resultado[3] = Puntaje)
            resultado = self.leer_datos(self.RankingA)
            puntaje = resultado[3]
            puntaje = int(puntaje)
            i = 0  # Utilizada para moverme atraves del diccionario.
            while resultado[3] != MAX and i < len(self.scoreItems):
                if puntaje > self.scoreItems[i][1][0]:
                    resultadoStr = ",".join(resultado) + "\n"
                    self.RankingB.write(resultadoStr)
                    resultado = self.leer_datos(self.RankingA)
                    puntaje = resultado[3]
                    puntaje = int(puntaje)
                if puntaje < self.scoreItems[i][1][0]:
                    linea = self.fecha + ',' + str(self.tiempo) + ',' + str(self.scoreItems[i][0]) + ',' + str(
                        self.scoreItems[i][1][0]) + ',' + str(self.scoreItems[i][1][1]) + "\n"
                    self.RankingB.write(linea)
                    puntaje = resultado[3]
                    puntaje = int(puntaje)
                    i += 1
                elif puntaje == self.scoreItems[i][1][0]:
                    linea = self.fecha + ',' + str(self.tiempo) + ',' + str(self.scoreItems[i][0]) + ',' + str(
                        self.scoreItems[i][1][0]) + ',' + str(self.scoreItems[i][1][1]) + "\n"
                    resultadoStr = ",".join(resultado) + "\n"
                    self.RankingB.write(resultadoStr)
                    self.RankingB.write(linea)
                    resultado = self.leer_datos(self.RankingA)
                    i += 1
            if resultado[3] != MAX:  # En caso de queden resultados aun sin escribir
                while resultado[3] != MAX:
                    resultadoStr = ",".join(resultado) + "\n"
                    self.RankingB.write(resultadoStr)
                    resultado = self.leer_datos(self.RankingA)
            elif resultado[3] == MAX and i < len(self.scoreItems):
                linea = self.fecha + ',' + str(self.tiempo) + ',' + str(self.scoreItems[i][0]) + ',' + str(
                    self.scoreItems[i][1][0]) + ',' + str(self.scoreItems[i][1][1]) + "\n"
                self.RankingB.write(linea)
                i += 1
            self.RankingA.close()
            self.RankingB.close()
            remove("partidasA.csv")
            rename("partidasB.csv", "partidasA.csv")

    def leer_datos(self, f):
        datos = f.readline()
        if datos:
            datos = datos.rstrip("\n").split(",")
        else:
            datos = "", "", "", MAX, ""
        return datos

    """
        PRE: Agrega a los jugadores de partidas anteriores de mayor a menor
        POST:
        Leandro.A.Peñaloza
    """

    def resumen(self):
        self.RankingA = open("partidasA.csv", "r")
        resultado = self.leer_datos(self.RankingA)
        iD = self.treeview.get_children()
        cantidad = 0
        while resultado[3] != MAX and cantidad < (len(iD)):
            self.treeview.item(iD[cantidad], values=resultado[1:5])
            resultado = self.leer_datos(self.RankingA)
            cantidad += 1
        while resultado[3] != MAX:
            self.treeview.insert(
                "", END, text=resultado[0], values=resultado[1:5])
            resultado = self.leer_datos(self.RankingA)
        
        messagebox.showinfo("Importante", "Juego Terminado")
        self.boton["state"] = DISABLED
        self.RankingA.close()


# ----------------------------------------------------------------------------------------------------------------------------------- #

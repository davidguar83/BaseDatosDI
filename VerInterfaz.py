import gi
import sqlite3 as dbapi
import os

from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from conexionBD import ConexionBD

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class Ventana():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("INTERFAZDI.glade")

        sinais = {"gtk_main_quit": self.on_cerrar,

                  "on_salirpro_clicked": self.btn_salir,
                  "on_salircli_clicked": self.btn_salir,
                  "on_salirven_clicked": self.btn_salir,
                  "on_ingresarcli_clicked": self.btn_ingrasar_cli,
                  "on_mostardatoscli_clicked": self.btn_consulta_cli,
                  "on_modificardeudacli_clicked": self.btn_modi_deuda_cli,
                  "on_borrardatoscli_clicked": self.btn_borrar_cli,
                  "on_limpiarcli_clicked": self.btn_limpiar,
                  "on_ingrasarpro_clicked": self.btn_ingrasar_pro,
                  "on_mostrarpro_clicked": self.btn_consulta_pro,
                  "on_modificarpvppro_clicked": self.btn_modi_pvp_pro,
                  "on_borrarpro_clicked": self.btn_borrar_pro,
                  "on_limpiarpro_clicked": self.btn_limpiar,
                  "on_ingresarven_clicked": self.btn_ingresar_ven,
                  "on_mostrardatosven_clicked": self.btn_consulta_ven,
                  "on_modificarcantven_clicked": self.btn_modi_cantidad_ven,
                  "on_borrarven_clicked": self.btn_borrar_ven,
                  "on_limpiarven_clicked": self.btn_limpiar,

                  }

        builder.connect_signals(sinais)

        # ventana cliente txt y treeVied---------------------------------------------------------------------------------

        self.txtdni = builder.get_object("txtdni")
        self.txtnombre = builder.get_object("txtnombre")
        self.txtapellidos = builder.get_object("txtapellidos")
        self.txttelefono = builder.get_object("txttelefono")
        self.txtdeuda = builder.get_object("txtdeuda")
        self.txtcomentarios = builder.get_object("txtcomentarios")
        self.treeView = builder.get_object("treeviewcli")

        modelo_tabla = Gtk.ListStore(str, str, str, int, int)

        baseDatos = ConexionBD("baseDI.dat")
        listaClientes = baseDatos.consultaSenParametros("SELECT * FROM clientes")

        for cliente in listaClientes:
            modelo_tabla.append(cliente)

            # objeto seleccin que utilizamos para el boton añadir cliente

        #treeVCli = Gtk.TreeView(modelo_tabla)
        self.seleccion = self.treeView.get_selection()
        self.seleccion.connect("changed", self.treevcli_selec_ingresar)

        for x, columnas in enumerate(["DNI", "Nombre", "Apellidos", "Telefono", "Deuda"]):
            celda = Gtk.CellRendererText()
            columnacli = Gtk.TreeViewColumn(columnas, celda, text=x)
            celda.props.editable = True
            # celda.set_property("editable",True)
            celda.connect("edited", self.celda_edit, x, modelo_tabla)
            # ordenar las columnas por valor
            columnacli.set_sort_column_id(x)
            self.treeView.append_column(columnacli)
        self.treeView.set_model(modelo_tabla)
        self.treeView.set_reorderable(True)

        # ventana provedor txt y treeweiv---------------------------------------------------------------------

        self.txtrefpro = builder.get_object("txtrefpro")
        self.txtnombrepro = builder.get_object("txtnombrepro")
        self.txtxpvppro = builder.get_object("txtxpvppro")
        self.txtcomentariospro = builder.get_object("txtcomentariospro")
        self.treeViedpro = builder.get_object("treeviewpro")

        baseDatos = ConexionBD("baseDI.dat")
        modelo_tabla_pro = Gtk.ListStore(int, str, float)
        listaPro = baseDatos.consultaSenParametros("SELECT * FROM productos")
        for produc in listaPro:
            modelo_tabla_pro.append(produc)

        #treeVPro = Gtk.TreeView(modelo_tabla_pro)
        self.seleccionpro = self.treeViedpro.get_selection()
        self.seleccionpro.connect("changed", self.treevpro_selec_chan)

        self.treeViedpro.set_model(modelo_tabla_pro)
        for x, columpro in enumerate(["Referen", "Nombre", "P.V.P."]):
            celdapro = Gtk.CellRendererText()
            colpro = Gtk.TreeViewColumn(columpro, celdapro, text=x)
            celdapro.props.editable = True
            celdapro.connect("edited", self.on_celda_edite, x, modelo_tabla_pro)
            colpro.set_sort_column_id(x)
            self.treeViedpro.append_column(colpro)
        self.treeViedpro.set_reorderable(True)

        # ventana ventas txt-------------------------------------------------------------------------

        self.txtrefven = builder.get_object("txtrefven")
        self.txtnombreven = builder.get_object("txtnombreven")
        self.txtcanven = builder.get_object("txtcanven")
        self.txtcomentariosven = builder.get_object("txtcomentariosven")
        self.treeViedven = builder.get_object("treeviewven")

        baseDatos = ConexionBD("baseDI.dat")
        modelo_tabla_ven = Gtk.ListStore(int, str, int)
        listaVen = baseDatos.consultaSenParametros("SELECT * FROM ventas")

        for produc in listaVen:
            modelo_tabla_ven.append(produc)

        #treeVVen = Gtk.TreeView(modelo_tabla_ven)
        self.seleccionVen = self.treeViedven.get_selection()
        self.seleccionVen.connect("changed", self.treevVen_selec_chan)

        self.treeViedven.set_model(modelo_tabla_ven)

        for x, columpro in enumerate(["Referencia", "Nombre", "Cantidad"]):
            celdaven = Gtk.CellRendererText()
            colven = Gtk.TreeViewColumn(columpro, celdaven, text=x)
            colven.set_sort_column_id(x)

            celdaven.props.editable = True

            celdaven.connect("edited", self.celda_change, x, modelo_tabla_ven)

            self.treeViedven.append_column(colven)

        self.treeViedven.set_reorderable(True)

        VentanaDatos = builder.get_object("VentanaDatos")
        VentanaDatos.show_all()

    def celda_edit(self, celda, fila, texto, columna, modelo):
        modelo[fila][columna] = texto

    def celda_change(self, celda, fila, texto, columna, modelo):

        modelo[fila][columna] = texto

    def on_celda_edite(self, celda, fila, texto, columna, modelo):
        modelo[fila][columna] = texto

    def treevcli_selec_ingresar(self):

        modelo, fila = self.seleccion.get_selected()
        if fila is not None:
            self.txtdni.set_text(modelo[fila][0])
            self.txtnombre.set_text(modelo[fila][1])
            self.txtapellidos.set_text(modelo[fila][2])
            self.txttelefono.set_text(str(modelo[fila][3]))
            self.txtdeuda.set_text(str(modelo[fila][4]))


    def treevpro_selec_chan(self):

        modelo, fila = self.seleccionpro.get_selected()
        if fila is not None:
            self.txtrefpro.set_text(str(modelo[fila][0]))
            self.txtnombrepro.set_text(modelo[fila][1])
            self.txtxpvppro.set_text(str(modelo[fila][2]))

    def treevVen_selec_chan(self):

        modelo, fila = self.seleccionVen.get_selected()
        if fila is not None:
            self.txtrefven.set_text(str(modelo[fila][0]))
            self.txtnombreven.set_text(modelo[fila][1])
            self.txtcanven.set_text(str(modelo[fila][2]))

    def btn_ingrasar_cli(self, boton):

        """inserta una funcion y sus argumentos en el grupo de procesoso.

        La entrada se inserta en las colas de forma rotatoria.
        Cada trabajo es identificado por un indice que devuelve la funcion.
        No todos los parametros del multiprocesamiento original.
        Pool.apply_aync se han implementado hasta ahora

        :param func:Funcion a procesar.
        :type func:invocable.
        :param args:Argumentos para que la funcion procese.
        :types args:Tuple.
        :returns:Lista de datos clientes.
        :rtype:str,int
        """
        modelo_tabla, fila = self.seleccion.get_selected()
        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)
        consulta = list()
        if len(listaClientes) == 0:
            consulta.append(self.txtdni.get_text())
            consulta.append(self.txtnombre.get_text())
            consulta.append(self.txtapellidos.get_text())
            consulta.append(int(self.txttelefono.get_text()))
            consulta.append(int(self.txtdeuda.get_text()))
            # metodo conexinDB
            baseDatos.ingresarCliente(consulta)
            self.txtcomentarios.set_text("Operacion OK")
            modelo_tabla.append(consulta)
        else:
            self.txtcomentarios.set_text("DNI duplicado")
            print("dni duplicado")

    def btn_ingrasar_pro(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.

                La entrada se inserta en las colas de forma rotatoria.
                Cada trabajo es identificado por un indice que devuelve la funcion.
                No todos los parametros del multiprocesamiento original.
                Pool.apply_aync se han implementado hasta ahora

                :param func:Funcion a procesar.
                :type func:invocable.
                :param args:Argumentos para que la funcion procese.
                :types args:Tuple.
                :returns:Lista de datos clientes.
                :rtype:str,int
                """
        modelo_tabla_pro, fila = self.seleccionpro.get_selected()
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)
        consulta2 = list()
        if len(listaClientes) == 0:
            consulta2.append(int(self.txtrefpro.get_text()))
            consulta2.append(self.txtnombrepro.get_text())
            consulta2.append(float(self.txtxpvppro.get_text()))
            # metodo conexinDB
            baseDatos.ingresarProducto(consulta2)

            self.txtcomentariospro.set_text("Operacion OK")
            modelo_tabla_pro.append(consulta2)
        else:

            self.txtcomentariospro.set_text("REF. duplicado")
            print("REF. duplicado")

        # print("boton funciona")

    def btn_ingresar_ven(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.

                La entrada se inserta en las colas de forma rotatoria.
                Cada trabajo es identificado por un indice que devuelve la funcion.
                No todos los parametros del multiprocesamiento original.
                Pool.apply_aync se han implementado hasta ahora

                :param func:Funcion a procesar.
                :type func:invocable.
                :param args:Argumentos para que la funcion procese.
                :types args:Tuple.
                :returns:Lista de datos clientes.
                :rtype:str,int
                """

        modelo_tabla_ven, fila = self.seleccionVen.get_selected()

        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefven.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", ref)

        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        consulta3 = list()

        if is_emply(listaClientes) == True:
            consulta3.append(int(self.txtrefven.get_text()))
            consulta3.append(self.txtnombreven.get_text())
            consulta3.append(int(self.txtcanven.get_text()))

            # metodo conexinDB

            baseDatos.ingresarVentas(consulta3)

            self.txtcomentariosven.set_text("Operacion OK")
            modelo_tabla_ven.append(consulta3)

        else:

            self.txtcomentariosven.set_text("REF. duplicado")
            print("REF. duplicado")

        # print("boton funciona")
        # self.txtcomentariosven.set_text("Operacion OK")

    def btn_limpiar(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.


                Metodo que dirve para vaciar los txt de todas las ventanas.

                :param func:Funcion a procesar.
                :type func:invocable.
                :param args:Argumentos para que la funcion procese.
                :types args:Objetos txt
                :returns:Objetos txt vacios
                :rtype:null
                """

        self.txtdni.set_text("")
        self.txtnombre.set_text("")
        self.txtapellidos.set_text("")
        self.txtdeuda.set_text("")
        self.txttelefono.set_text("")
        self.txtcomentarios.set_text("operacion realizada")
        self.txtcomentariospro.set_text("operacion realizada")
        self.txtcomentariosven.set_text("operacion realizada")
        self.txtrefpro.set_text("")
        self.txtrefven.set_text("")
        self.txtnombrepro.set_text("")
        self.txtnombreven.set_text("")
        self.txtxpvppro.set_text("")
        self.txtcanven.set_text("")

    def btn_consulta_cli(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.

                        Metodo que nos devuelve una Tupla con el dato a verificar.
                        El dato se casa del un txt.
                        Se envia a otra clase para que realice la consulta.
                        Nos devuelve una Tupla.

                        :param func:Funcion a procesar.
                        :type func:invocable.
                        :param args:Argumentos para que la funcion procese.
                        :types args:Tuple.
                        :returns:Lista de datos clientes.
                        :rtype:str,int
                        """

        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)

        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        if is_emply(listaClientes) == True:
            self.txtcomentarios.set_text("Dni no valido")

        for consulta in listaClientes:
            self.txtnombre.set_text(consulta[1])
            self.txtapellidos.set_text(consulta[2])
            self.txtdeuda.set_text(str(consulta[4]))
            self.txttelefono.set_text(str(consulta[3]))
            self.txtcomentarios.set_text("consulta realizada")

        # print(listaClientes)

    def btn_consulta_pro(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.

                                Metodo que nos devuelve una Tupla con el dato a verificar.
                                El dato se casa del un txt.
                                Se envia a otra clase para que realice la consulta.
                                Nos devuelve una Tupla.

                                :param func:Funcion a procesar.
                                :type func:invocable.
                                :param args:Argumentos para que la funcion procese.
                                :types args:Tuple.
                                :returns:Lista de datos clientes.
                                :rtype:str,int
                                """
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaproductos = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)

        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        if is_emply(listaproductos) == True:
            print("hola")

            self.txtcomentariospro.set_text("REF no valido")

        for conpro in listaproductos:
            self.txtnombrepro.set_text(conpro[1])
            self.txtxpvppro.set_text(str(conpro[2]))

            self.txtcomentariospro.set_text("consulta realizada")

        # self.txtcomentariospro.set_text("consulta realizada")

    def btn_consulta_ven(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.

                                Metodo que nos devuelve una Tupla con el dato a verificar.
                                El dato se casa del un txt.
                                Se envia a otra clase para que realice la consulta.
                                Nos devuelve una Tupla.

                                :param func:Funcion a procesar.
                                :type func:invocable.
                                :param args:Argumentos para que la funcion procese.
                                :types args:Tuple.
                                :returns:Lista de datos clientes.
                                :rtype:str,int
                                """
        baseDatos = ConexionBD("baseDI.dat")
        refven = self.txtrefven.get_text()
        listaven = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", refven)

        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        if is_emply(listaven) == True:
            self.txtcomentariosven.set_text("REF no valido")
        for conven in listaven:
            self.txtnombreven.set_text(conven[1])
            self.txtcanven.set_text(str(conven[2]))
            self.txtcomentariosven.set_text("consulta realizada")

    def btn_modi_deuda_cli(self, boton):

        modelo, fila = self.seleccion.get_selected()
        modelo.remove(fila)
        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)
        consulta2 = list()
        if len(listaClientes) != 0:
            consulta2.append(self.txtdni.get_text())
            consulta2.append(self.txtnombre.get_text())
            consulta2.append(self.txtapellidos.get_text())
            consulta2.append(self.txttelefono.get_text())
            consulta2.append(self.txtdeuda.get_text())
            # metodo conexinDB
            baseDatos.modificarCliente(consulta2)
            self.txtcomentarios.set_text("Operacion OK")
            consulta=list()
            consulta.append(self.txtdni.get_text())
            consulta.append(self.txtnombre.get_text())
            consulta.append(self.txtapellidos.get_text())
            consulta.append(int(self.txttelefono.get_text()))
            consulta.append(int(self.txtdeuda.get_text()))
            modelo.append(consulta)
        else:
            self.txtcomentarios.set_text("DNI no existe")
            print("dni no existe")

    def btn_modi_pvp_pro(self, boton):
        """inserta una funcion y sus argumentos en el grupo de procesoso.

                                Metodo que permite modificar los atos en la base de datos
                                Tambien el el TreeView

                                :param func:Funcion a procesar.
                                :type func:invocable señal boton
                                :param args:Argumentos para que la funcion procese.
                                :types args:Tuple.
                                :returns:Lista de datos clientes.
                                :rtype:str,int
                                """
        modelo, fila = self.seleccionpro.get_selected()
        modelo.remove(fila)
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)
        consulta = list()
        if len(listaClientes) != 0:
            consulta.append(self.txtrefpro.get_text())
            consulta.append(self.txtnombrepro.get_text())
            consulta.append(self.txtxpvppro.get_text())
            # metodo conexinDB
            baseDatos.modificarProductos(consulta)
            self.txtcomentariospro.set_text("Modificacion  OK")
            consulta2 = list()
            consulta2.append(int(self.txtrefpro.get_text()))
            consulta2.append(self.txtnombrepro.get_text())
            consulta2.append(float(self.txtxpvppro.get_text()))
            modelo.append(consulta2)

        else:
            self.txtcomentariospro.set_text("REF no existe")
            print("REF no existe")

    def btn_modi_cantidad_ven(self, boton):
        modelo, fila = self.seleccionVen.get_selected()
        modelo.remove(fila)
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefven.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", ref)
        consulta = list()
        if len(listaClientes) != 0:
            consulta.append(self.txtrefven.get_text())
            consulta.append(self.txtnombreven.get_text())
            consulta.append(self.txtcanven.get_text())
            # metodo conexinDB
            baseDatos.modificarVentas(consulta)
            self.txtcomentariosven.set_text("Modificacion OK")
            consulta3 = list()
            consulta3.append(int(self.txtrefven.get_text()))
            consulta3.append(self.txtnombreven.get_text())
            consulta3.append(int(self.txtcanven.get_text()))
            modelo.append(consulta3)

        else:
            self.txtcomentariosven.set_text("REF no existe")
            print("REF no existe")

    def btn_borrar_cli(self, boton):
        """
        inserta una funcion y sus argumentos en el grupo de procesoso.

        Metodo para eliminar datos completos.
        Base datos y TreeView
        :paramfunc:Funcion a procesar.
        :typefunc:invocable.
        :paramargs:Argumentos para que la funcion procese.
        :typesargs:Tuple.
        :returns:Lista de datos clientes.
        :rtype:str,int
        """

        """(modelo,panhlist) = self.treeView.get_selection_rows()
        for panh in panhlist:
            iter=modelo.get_iter(panh)
            modelo.remove(iter)

        baseDatos = ConexionBD("baseDI.dat")
        listaClientes = baseDatos.consultaSenParametros("SELECT * FROM clientes")
        dni = self.txtdni.get_text()
        x=0

        for i in listaClientes:
            x+1
            if dni==listaClientes[0]:

                modelo, fila = self.seleccion.set_selected(self.modelo_tabla,x )
                modelo.remove(fila)

        for x, columnas in enumerate(listaClientes):
            if dni == listaClientes[0]:
                modelo.remove(x)"""

        modelo, fila = self.seleccion.get_selected()
        modelo.remove(fila)

        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)

        if len(listaClientes) == 0:

            self.txtcomentarios.set_text("Dni no existe")

        else:

            baseDatos.borrarCliente(dni)


            self.txtcomentarios.set_text("Cliente borrado")


    def btn_borrar_pro(self, boton):

        modelo, fila = self.seleccionpro.get_selected()
        modelo.remove(fila)

        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)



        if len(listaClientes) == 0:

            self.txtcomentariospro.set_text("REF no existe")

        else:

            baseDatos.borrarProvedor(ref)


            self.txtcomentariospro.set_text("Producto borrado")


    def btn_borrar_ven(self, boton):

        modelo, fila = self.seleccionVen.get_selected()
        modelo.remove(fila)

        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefven.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", ref)



        if len(listaClientes) == 0:

            self.txtcomentariosven.set_text("REF no existe")

        else:


            baseDatos.borrarVentas(ref)


            self.txtcomentariosven.set_text("Producto venta borrado")


    def on_cerrar(self):
        Gtk.main_quit()

    def btn_salir(self, boton):
        estiloHoja = getSampleStyleSheet()
        story = []

        fich_imagen = "/home/sparrow/PycharmProjects/BaseDatosDI/Base_Datos.jpg"
        imagen_logo = Image(os.path.relpath(fich_imagen), width=400, height=100)
        story.append(imagen_logo)

        cabecera = estiloHoja['Heading4']
        cabecera.pageBreakBefore = 0
        cabecera.keepWithNext = 0
        cabecera.backColor = colors.green

        parrafo = Paragraph("Bade de Datos DI", cabecera)
        story.append(parrafo)

        cadena = " Datos de Clientes"

        estilo = estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        story.append(parrafo2)

        story.append(Spacer(0, 20))

        doc = SimpleDocTemplate("Informe.pdf", pagesize=A4, showBoundary=1)

        story.append(Spacer(0, 20))

        listacli = []
        listacli.append(("DNI", "NOMBRE", "APELLIDO", "TELEF", "DEUDA"))
        listapro = []
        listapro.append(("REF", "NOMBRE", "PVP"))
        listaven = []
        listaven.append(("REF", "NOMBRE", "CANTIDAD"))

        try:

            conexion = dbapi.connect("baseDI.dat")

        except dbapi.StandardError as e:

            print(e)
        else:

            print("Base conectada")

        try:

            cursor = conexion.cursor()
            cursor.execute("select * from clientes")
            for fila in cursor.fetchall():
                listacli.append(fila)

            cursor.execute("select * from productos")
            for filapro in cursor.fetchall():
                listapro.append(filapro)

            cursor.execute("select * from ventas")
            for filaven in cursor.fetchall():
                listaven.append(filaven)


        except dbapi.DatabaseError as e:

            print("Error en consulta cliente: " + str(e))

        else:
            print("Consulta realizada")

        finally:
            cursor.close()
            conexion.close()

        tablacli = Table(listacli)

        tablacli.setStyle([('TEXTCOLOR', (0, 0), (-1, 0), colors.blueviolet)])
        tablacli.setStyle([('BACKGROUND', (0, 1), (-1, -1), colors.greenyellow)])
        tablacli.setStyle([('BOX', (0, 1), (-1, -1), 0.25, colors.black)])
        tablacli.setStyle([('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black)])

        story.append(tablacli)

        story.append(Spacer(0, 20))

        cadena = " Datos de Producto"
        estilo = estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        story.append(parrafo2)

        story.append(Spacer(0, 20))

        tablapro = Table(listapro)

        tablapro.setStyle([('TEXTCOLOR', (0, 0), (-1, 0), colors.blueviolet)])
        tablapro.setStyle([('BACKGROUND', (0, 1), (-1, -1), colors.greenyellow)])
        tablapro.setStyle([('BOX', (0, 1), (-1, -1), 0.25, colors.black)])
        tablapro.setStyle([('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black)])
        story.append(tablapro)

        story.append(Spacer(0, 20))

        cadena = " Datos de Producto Ventas"
        estilo = estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        story.append(parrafo2)

        story.append(Spacer(0, 20))

        tablaven = Table(listaven)

        tablaven.setStyle([('TEXTCOLOR', (0, 0), (-1, 0), colors.blueviolet)])
        tablaven.setStyle([('BACKGROUND', (0, 1), (-1, -1), colors.greenyellow)])
        tablaven.setStyle([('INNERGIRD', (0, 1), (-1, -1), 0.25, colors.blueviolet)])
        tablaven.setStyle([('BOX', (0, 1), (-1, -1), 0.25, colors.black)])
        tablaven.setStyle([('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black)])
        story.append(tablaven)

        doc.build(story)





        print("boton pulsado")
        self.on_cerrar()


if __name__ == "__main__":
    Ventana()
    Gtk.main()




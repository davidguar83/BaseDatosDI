

import gi
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

        # ventana cliente txt y treeVied

        self.txtdni = builder.get_object("txtdni")
        self.txtnombre = builder.get_object("txtnombre")
        self.txtapellidos = builder.get_object("txtapellidos")
        self.txttelefono = builder.get_object("txttelefono")
        self.txtdeuda = builder.get_object("txtdeuda")
        self.txtcomentarios = builder.get_object("txtcomentarios")
        self.treeView = builder.get_object("treeviewcli")



        # ventana provedor txt y treeweiv

        self.txtrefpro = builder.get_object("txtrefpro")
        self.txtnombrepro = builder.get_object("txtnombrepro")
        self.txtxpvppro = builder.get_object("txtxpvppro")
        self.txtcomentariospro = builder.get_object("txtcomentariospro")
        self.treeViedpro = builder.get_object("treeviewpro")


        # ventana ventas txt

        self.txtrefven = builder.get_object("txtrefven")
        self.txtnombreven = builder.get_object("txtnombreven")
        self.txtcanven = builder.get_object("txtcanven")
        self.txtcomentariosven = builder.get_object("txtcomentariosven")
        self.treeViedven = builder.get_object("treeviewven")


        self.montatreeWievCli()
        self.montatreeWievPro()
        self.montatreeWievVen()

        self.visualizarTreeWeiv()

        VentanaDatos = builder.get_object("VentanaDatos")
        VentanaDatos.show_all()

    def on_cerrar(self):
        Gtk.main_quit()

    def btn_salir(self, boton):

        print("boton pulsado")
        self.on_cerrar()

    def btn_ingrasar_cli(self, boton):
        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)
        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False




        #print(is_emply(listaClientes))

        consulta = list()

        if is_emply(listaClientes) == True:
            consulta.append(self.txtdni.get_text())
            consulta.append(self.txtnombre.get_text())
            consulta.append(self.txtapellidos.get_text())
            consulta.append(self.txttelefono.get_text())
            consulta.append(self.txtdeuda.get_text())


            #metodo conexinDB

            baseDatos.ingresarCliente(consulta)

            self.txtcomentarios.set_text("Operacion OK")


            self.montatreeWievCli()

        else:
                self.txtcomentarios.set_text("DNI duplicado")
                print("dni duplicado")

    def btn_ingrasar_pro(self, boton):
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)

        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        consulta = list()

        if is_emply(listaClientes) == True:
            consulta.append(self.txtrefpro.get_text())
            consulta.append(self.txtnombrepro.get_text())
            consulta.append(self.txtxpvppro.get_text())

            # metodo conexinDB

            baseDatos.ingresarProducto(consulta)

            #self.montatreeWievPro()

            self.txtcomentariospro.set_text("Operacion OK")


        else:

            self.txtcomentariospro.set_text("REF. duplicado")
            print("REF. duplicado")




        #print("boton funciona")





    def btn_ingresar_ven(self, boton):
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefven.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", ref)
        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False


        consulta = list()

        if is_emply(listaClientes) == True:
            consulta.append(self.txtrefven.get_text())
            consulta.append(self.txtnombreven.get_text())
            consulta.append(self.txtcanven.get_text())

            # metodo conexinDB

            baseDatos.ingresarVentas(consulta)

            self.txtcomentariosven.set_text("Operacion OK")
            #self.montatreeWievVen()

        else:

            self.txtcomentariosven.set_text("REF. duplicado")
            print("REF. duplicado")

        # print("boton funciona")
        #self.txtcomentariosven.set_text("Operacion OK")


    def btn_limpiar(self, boton):

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


        #self.txtcomentariospro.set_text("consulta realizada")

    def btn_consulta_ven(self, boton):
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
        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)
        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        consulta = list()

        if is_emply(listaClientes) == False:
            consulta.append(self.txtdni.get_text())
            consulta.append(self.txtnombre.get_text())
            consulta.append(self.txtapellidos.get_text())
            consulta.append(self.txttelefono.get_text())
            consulta.append(self.txtdeuda.get_text())

            # metodo conexinDB

            baseDatos.modificarCliente(consulta)

            self.txtcomentarios.set_text("Operacion OK")
            #self.montatreeWievCli()

        else:
            self.txtcomentarios.set_text("DNI no existe")
            print("dni no existe")





    def btn_modi_pvp_pro(self, boton):
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)
        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False


        # print(is_emply(listaClientes))

        consulta = list()

        if is_emply(listaClientes) == False:
            consulta.append(self.txtrefpro.get_text())
            consulta.append(self.txtnombrepro.get_text())
            consulta.append(self.txtxpvppro.get_text())

            # metodo conexinDB

            baseDatos.modificarProductos(consulta)

            self.txtcomentariospro.set_text("Modificacion  OK")
            #self.montatreeWievPro()

        else:
            self.txtcomentariospro.set_text("REF no existe")
            print("REF no existe")






    def btn_modi_cantidad_ven(self, boton):

        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefven.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", ref)
        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        # print(is_emply(listaClientes))

        consulta = list()

        if is_emply(listaClientes) == False:
            consulta.append(self.txtrefven.get_text())
            consulta.append(self.txtnombreven.get_text())
            consulta.append(self.txtcanven.get_text())

            # metodo conexinDB

            baseDatos.modificarVentas(consulta)

            self.txtcomentariosven.set_text("Modificacion OK")
            #self.montatreeWievVen()

        else:
            self.txtcomentariosven.set_text("REF no existe")
            print("REF no existe")



    def btn_borrar_cli(self, boton):



        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?", dni)
        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        if is_emply(listaClientes) == True:

            self.txtcomentarios.set_text("Dni no existe")

        else:

            for datodni in listaClientes:


                dni = datodni[0]




            baseDatos.borrarCliente(dni)

            self.txtcomentarios.set_text("Cliente borrado")
            #self.montatreeWievCli()


    def btn_borrar_pro(self, boton):

        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)



        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        if is_emply(listaClientes) == True:

            self.txtcomentariospro.set_text("REF no existe")

        else:

            for datoref in listaClientes:
                ref = datoref[0]

            baseDatos.borrarProvedor(ref)

            self.txtcomentariospro.set_text("Producto borrado")
            #self.montatreeWievPro()


    def btn_borrar_ven(self, boton):

        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefven.get_text()
        listaClientes = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", ref)



        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        if is_emply(listaClientes) == True:

            self.txtcomentariosven.set_text("REF no existe")

        else:

            for datoref in listaClientes:
                ref = datoref[0]

            baseDatos.borrarVentas(ref)

            self.txtcomentariosven.set_text("Producto venta borrado")
            #self.montatreeWievVen()


    def on_txt(self):

        print("")

    modelo_tabla = Gtk.ListStore(str, str, str, int, int)

    def montatreeWievCli(self):

        #self.treeView.Nodes.Clear()



        baseDatos = ConexionBD("baseDI.dat")



        listaClientes = baseDatos.consultaSenParametros("SELECT * FROM clientes")

        for cliente in listaClientes:
            self.modelo_tabla.append(cliente)

        def is_emply(compro):
            if len(compro) == 0:
                return True
            return False

        """if is_emply(listaClientes)==False:

            for cliente in listaClientes:
                self.modelo_tabla.append(cliente)



        else:


            self.modelo_tabla.delete()"""






        self.treeView.set_model(self.modelo_tabla)
        x = 0
        columnascli = ["DNI", "Nombre", "Apellidos", "Telefono", "Deuda"]

        for columnas in columnascli:
            celda = Gtk.CellRendererText()
            colcli = Gtk.TreeViewColumn(columnas, celda, text=x)
            celda.props.editable = True
            celda.connect("edited", self.on_celda_edite,x,self.modelo_tabla)

            #ordenar las columnas por valor

            colcli.set_sort_column_id(x)

            self.treeView.append_column(colcli)
            x = x + 1

        self.treeView.set_reorderable(True)
    # self.treeView.add(tablaCliente)


    def on_celda_edite(self,celda,fila,texto,columna,modelo):
        modelo [fila][columna] = texto







    def montatreeWievPro(self):

        columnaspro = ["Referen",
                       "Nombre",
                       "P.V.P."]

        baseDatos = ConexionBD("baseDI.dat")
        modelo_tabla_pro = Gtk.ListStore(int, str, int)
        listaPro = baseDatos.consultaSenParametros("SELECT * FROM productos")

        for produc in listaPro:
            modelo_tabla_pro.append(produc)

        self.treeViedpro.set_model(modelo_tabla_pro)

        x = 0

        for columpro in columnaspro:
            celdapro = Gtk.CellRendererText()
            colpro = Gtk.TreeViewColumn(columpro, celdapro, text=x)

            colpro.set_sort_column_id(x)
            self.treeViedpro.append_column(colpro)
            x = x + 1
        self.treeViedpro.set_reorderable(True)

    def montatreeWievVen(self):

        columnasven = ["Referencia",
                       "Nombre",
                       "Cantidad"]

        baseDatos = ConexionBD("baseDI.dat")
        modelo_tabla_ven = Gtk.ListStore(int, str, int)
        listaPro = baseDatos.consultaSenParametros("SELECT * FROM ventas")

        for produc in listaPro:
            modelo_tabla_ven.append(produc)

        self.treeViedven.set_model(modelo_tabla_ven)

        x = 0

        for columpro in columnasven:
            celdaven = Gtk.CellRendererText()
            colven = Gtk.TreeViewColumn(columpro, celdaven, text=x)
            colven.set_sort_column_id(x)
            self.treeViedven.append_column(colven)
            x = x + 1

        self.treeViedven.set_reorderable(True)


    def limpiarTreeCli(self):

        modelo_tabla = Gtk.ListStore(str, str, str, int, int)

        modelo_tabla.clear()

        self.treeView.set_model(modelo_tabla)


        x = 0
        columnascli = ["DNI", "Nombre", "Apellidos", "Telefono", "Deuda"]

        for columnas in columnascli:
            celda = Gtk.CellRendererText()
            colcli = Gtk.TreeViewColumn(columnas, celda, text=x)
            self.treeView.append_column(colcli)
            x = x + 1


    def visualizarTreeWeiv(self):

        registros = self.treeView.get_children()
        for registro in registros:
            print(registro[0])
            print("ooo")





if __name__ == "__main__":
    Ventana()
    Gtk.main()

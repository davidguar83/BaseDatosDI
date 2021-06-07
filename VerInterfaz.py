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
                  "on_btnsalir_clicked": self.btn_salir,
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

        # ventana cliente txt

        self.txtdni = builder.get_object("txtdni")
        self.txtnombre = builder.get_object("txtnombre")
        self.txtapellidos = builder.get_object("txtapellidos")
        self.txttelefono = builder.get_object("txttelefono")
        self.txtdeuda = builder.get_object("txtdeuda")
        self.txtcomentarios = builder.get_object("txtcomentarios")

        # ventana provedor txt

        self.txtrefpro = builder.get_object("txtrefpro")
        self.txtnombrepro = builder.get_object("txtnombrepro")
        self.txtxpvppro = builder.get_object("txtxpvppro")
        self.txtcomentariospro = builder.get_object("txtcomentariospro")

        # ventana ventas txt

        self.txtrefven = builder.get_object("txtrefven")
        self.txtnombreven = builder.get_object("txtnombreven")
        self.txtcanven = builder.get_object("txtcanven")
        self.txtcomentariosven = builder.get_object("txtcomentariosven")

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

            self.txtcomentariospro.set_text("Operacion OK")

        else:
            self.txtcomentariospro.set_text("REF. duplicado")
            print("REF. duplicado")




        #print("boton funciona")
        self.txtcomentariospro.set_text("Operacion OK")

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

        else:
            self.txtcomentariosven.set_text("REF. duplicado")
            print("REF. duplicado")

        # print("boton funciona")
        self.txtcomentariosven.set_text("Operacion OK")


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
        for consulta in listaClientes:
            self.txtnombre.set_text(consulta[1])
            self.txtapellidos.set_text(consulta[2])
            self.txtdeuda.set_text(str(consulta[4]))
            self.txttelefono.set_text(str(consulta[3]))

        # print(listaClientes)

        self.txtcomentarios.set_text("consulta realizada")

    def btn_consulta_pro(self, boton):
        baseDatos = ConexionBD("baseDI.dat")
        ref = self.txtrefpro.get_text()
        listaproductos = baseDatos.consultaConParametros("SELECT * FROM productos WHERE ref=?", ref)
        for conpro in listaproductos:
            self.txtnombrepro.set_text(conpro[1])
            self.txtxpvppro.set_text(str(conpro[2]))

        self.txtcomentariospro.set_text("consulta realizada")

    def btn_consulta_ven(self, boton):
        baseDatos = ConexionBD("baseDI.dat")
        refven = self.txtrefven.get_text()
        listaven = baseDatos.consultaConParametros("SELECT * FROM ventas WHERE ref=?", refven)
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

        # print(is_emply(listaClientes))

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

            self.txtcomentariospro.set_text("Operacion OK")

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

            self.txtcomentariosven.set_text("Operacion OK")

        else:
            self.txtcomentariosven.set_text("REF no existe")
            print("REF no existe")





        print("boton funciona")

    def btn_borrar_cli(self, boton):
        print("boton funciona")

    def btn_borrar_pro(self, boton):
        print("boton funciona")

    def btn_borrar_ven(self, boton):
        print("boton funciona")

    def on_txt(self):

        print("")


if __name__ == "__main__":
    Ventana()
    Gtk.main()

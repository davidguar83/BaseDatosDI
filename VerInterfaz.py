import gi
from conexionBD import ConexionBD
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

class Ventana():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("INTERFAZDI.glade")

        sinais={"gtk_main_quit": self.on_cerrar,

                "on_salirpro_clicked": self.btn_salir,
                "on_btnsalir_clicked": self.btn_salir,
                "on_salirven_clicked": self.btn_salir,
                "on_ingresarcli_clicked": self.btn_ingrasar_cli,
                "on_mostardatoscli_clicked" : self.btn_consulta_cli,
                "on_modificardeudacli_clicked": self.btn_modi_deuda_cli,
                "on_borrardatoscli_clicked": self.btn_borrar_cli,
                "on_limpiarcli_clicked": self.btn_limpiar,
                "on_ingrasarpro_clicked": self.btn_ingrasar_pro,
                "on_mostrarpro_clicked": self.btn_consulta_pro,
                "on_modificarpvppro_clicked": self.btn_modi_pvp_pro,
                "on_borrarpro_clicked": self.btn_borrar_pro,
                "on_limpiarpro_clicked": self.btn_limpiar,
                "on_ingresarven_clicked": self.btn_ingrasar_ven,
                "on_mostrardatosven_clicked": self.btn_consulta_ven,
                "on_modificarcantven_clicked": self.btn_modi_cantidad_ven,
                "on_borrarven_clicked": self.btn_borrar_ven,
                "on_limpiarven_clicked": self.btn_limpiar,
                "on_txtcomentarios_activate": self.on_txt,

        }

        builder.connect_signals (sinais)

        self.txtdni = builder.get_object ("txtdni")
        self.txtnombre = builder.get_object ("txtnombre")
        self.txtapellidos = builder.get_object ("txtapellidos")
        self.txttelefono = builder.get_object ("txttelefono")
        self.txtdeuda = builder.get_object ("txtdeuda")
        self.txtcomentarios = builder.get_object ("txtcomentarios")



        VentanaDatos = builder.get_object("VentanaDatos")
        VentanaDatos.show_all()

    def on_cerrar (self):
        Gtk.main_quit()



    def btn_salir(self,boton):

        print("boton pulsado")
        self.on_cerrar()


    def btn_ingrasar_cli(self,boton):

        print("boton funciona")

    def btn_ingrasar_pro(self, boton):
        print("boton funciona")

    def btn_ingrasar_ven(self, boton):
        print("boton funciona")

    def btn_limpiar(self, boton):

        self.txtdni.set_text("")
        self.txtnombre.set_text("")
        self.txtapellidos.set_text("")
        self.txtdeuda.set_text("")
        self.txttelefono.set_text("")


    def btn_consulta_cli(self, boton):

        baseDatos = ConexionBD("baseDI.dat")
        dni = self.txtdni.get_text()
        listaClientes=baseDatos.consultaConParametros("SELECT * FROM clientes WHERE dni=?",dni)
        for consulta in listaClientes:

          self.txtnombre.set_text(consulta[1])
          self.txtapellidos.set_text(consulta[2])
          self.txtdeuda.set_text(str(consulta[4]))
          self.txttelefono.set_text(str(consulta[3]))

       # print(listaClientes)

        self.txtcomentarios.set_text ("consulta realizada")

    def btn_consulta_pro(self, boton):
        print("boton funciona")


    def btn_consulta_ven(self, boton):
        print("boton funciona")

    def btn_modi_deuda_cli(self, boton):
        print("boton funciona")

    def btn_modi_pvp_pro(self, boton):
        print("boton funciona")

    def btn_modi_cantidad_ven(self, boton):
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
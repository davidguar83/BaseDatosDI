import gi
from conexionBD import ConexionBD
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

class Ventana():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("INTERFAZDI.glade")

        sinais={"gtk_main_quit": self.on_cerrar,
                "on_btnsalir_clicked": self.on_btn_salir,


        }

        builder.connect_signals (sinais)

        VentanaDatos = builder.get_object("VentanaDatos")
        VentanaDatos.show_all()

    def on_cerrar (self):
        Gtk.main_quit()



    def on_btn_salir(self,boton):

        print("boton pulsado")
        self.on_cerrar()



if __name__ == "__main__":
    Ventana()
    Gtk.main()
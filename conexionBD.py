import sqlite3 as dbapi


class ConexionBD:
    """Clase para realizar a conexión a una base de datos SQlite.

    """

    def __init__(self,rutaBd):

        """Crea as propiedades e as inicializa

        :param rutaBd: Ruta onde se encontra o ficheiro da base de datos SQlite

        """
        self.rutaBd = rutaBd
        self.conexion = dbapi.connect ("baseDI.dat")
        self.cursor = self.conexion.cursor()


    def conectaBD (self):
        """Método que crea a conexión da base de datos.

        Para realizar a conexión precisa da ruta onde está a base de datos que pásaselle no método __init__.

        """

        try:
            if self.conexion is None:
                if self.rutaBd is None:
                    print ("A ruta da base de datos é: None ")
                else:
                    self.conexion = dbapi.connect (self.rutaBd)
            else:
                print ("Base de datos conectada: " + self.conexion)

        except dbapi.StandardError as e:
            print ("Erro o facer a conexión a base de datos " + self.rutaBd + ": " + e)
        else:
            print ("Conexión de base de datos realizada")


    def creaCursor(self):
        """Método que crea o cursor da base de datos.

        Para realizar o cursor precísase previamente da execución do método conectaBD, que crea a conexión a base de
        datos na ruta onde está padada o método __init__.

        """

        try:
            if self.conexion is None:
                print ("Creando o cursor: É necesario realizar a conexión a base de datos previamente")


            else:
                if self.cursor is None:
                    self.cursor = self.conexion.cursor()
                else:
                    print ("O cursor xa esta inicializado: " + self.cursor)


        except dbapi.Error as e:
            print (e)
        else:
            print ("Cursor preparado")


    def consultaSenParametros (self, consultaSQL):
        """Retorna unha lista cos rexistros dunha consulta realizada sen pasarlle parámetros.

        :param consultaSQL. Código da consulta sql a executar
        :return listaConsulta

        """

        listaConsulta = list()
        try:
            if self.conexion is None:
                print("Creando consulta: É necesario realizar a conexión a base de datos previamente")
            else:
                if self.cursor is None:
                    print("Creando consulta: É necesario realizar a creación do cursor previamente")
                else:
                    self.cursor.execute(consultaSQL)

                    for fila in self.cursor.fetchall():
                        listaConsulta.append (fila)

        except dbapi.DatabaseError as e:
            print("Erro facendo a consulta: " + str(e))
            return None
        else:
            print("Consulta executada")
            return listaConsulta

    def consultaConParametros(self, consultaSQL, *parametros):
        """Retorna unha lista cos rexistros dunha consulta realizada pasandolle os parámetros.

        A consulta ten que estar definida con '?' na clausula where de SQL.

        :param consultaSQL. Código da consulta sql a executar
        :param *parametros. Lista de parámetros para introducir na consulta
        :return listaConsulta

        """

        listaConsulta = list()
        try:
            if self.conexion is None:
                print("Creando consulta: É necesario realizar a conexión a base de datos previamente")
            else:
                if self.cursor is None:
                    print("Creando consulta: É necesario realizar a creación do cursor previamente")
                else:


                    self.cursor.execute(consultaSQL, parametros)

                    for fila in self.cursor.fetchall():
                        listaConsulta.append(fila)

        except dbapi.DatabaseError as e:
            print("Erro facendo a consulta: " + str(e))
            return None
        else:
            print("Consulta executada")
            return listaConsulta


    def ingresarCliente(self,listarecibida):

        try:
            if self.conexion is None:
                print("Creando consulta: É necesario realizar a conexión a base de datos previamente")
            else:
                if self.cursor is None:
                    print("Creando consulta: É necesario realizar a creación do cursor previamente")
                else:

                    lista = listarecibida

                    self.cursor.execute("INSERT INTO clientes VALUES( '" + lista[0] +
                                        "' , '" + lista[1] +
                                        "' , '" + lista[2] +
                                        "' , " + str(lista[3]) +
                                        " , " + str(lista[4]) + ")")

        except dbapi.DatabaseError as e:
            print("Erro facendo insert cliente: " + str(e))
            return None
        else:
            print("Operacion executada")

            self.conexion.commit()

    def is_emply(compro):
        if len(compro) == 0:
            return True
        return False

    def ingresarProducto(self,listarecibida):

        try:
            if self.conexion is None:
                print("Creando consulta: É necesario realizar a conexión a base de datos previamente")
            else:
                if self.cursor is None:
                    print("Creando consulta: É necesario realizar a creación do cursor previamente")
                else:

                    listaP = listarecibida

                    self.cursor.execute("INSERT INTO productos VALUES( " + str(listaP[0])+
                                        " , '" + listaP[1] +
                                        "' , " + str(listaP[2]) + ")")

        except dbapi.DatabaseError as e:
            print("Erro facendo o insert producto: " + str(e))
            return None
        else:
            print("Operacion executada")
            self.conexion.commit()



    def ingresarVentas(self,listarecibida):

        try:
            if self.conexion is None:
                print("Creando consulta: É necesario realizar a conexión a base de datos previamente")
            else:
                if self.cursor is None:
                    print("Creando consulta: É necesario realizar a creación do cursor previamente")
                else:

                    listaV = listarecibida

                    self.cursor.execute("INSERT INTO ventas VALUES( " + str(listaV[0])+
                                        " , '" + listaV[1] +
                                        "' , " + str(listaV[2]) + ")")

        except dbapi.DatabaseError as e:
            print("Erro facendo o insert ventas: " + str(e))
            return None
        else:
            print("Operacion executada")
            self.conexion.commit()


    def modificarCliente(self,listarecibida):

        try:
            if self.conexion is None:
                print("Creando consulta: É necesario realizar a conexión a base de datos previamente")
            else:
                if self.cursor is None:
                    print("Creando consulta: É necesario realizar a creación do cursor previamente")
                else:

                    lista = listarecibida
                    print("hola")

                    dni = lista[0]

                    self.cursor.execute("UPDATE clientes SET nome= '"+lista[1]+"' WHERE DNI= '"+dni+"'")




        except dbapi.DatabaseError as e:
            print("Erro facendo insert cliente: " + str(e))
            return None
        else:
            print("Operacion executada")

            self.conexion.commit()



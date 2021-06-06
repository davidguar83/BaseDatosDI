import sqlite3 as dbapi

try:
    baseconexion = dbapi.connect ("baseDI.dat")
    print (baseconexion)


except dbapi.StandardError as e:
    print (e)
else:
    print ("Base de datos aberta")

try:
    cursor = baseconexion.cursor ()
    print (cursor)

except dbapi.Error as e:
    print (e)
else:
    print ("Cursor preparado")


def ingresarCliente(listarecibida):

    lista = listarecibida()

    cursor.execute("insert into clientes values( '" + lista[0]+
    "' , '" + lista[1]+
    "' , '" + lista[2]+
    "' , '" + str(lista[3])+
    "' , '" + str(lista[4])+"')")

    baseconexion.commit()






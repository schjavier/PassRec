#!/usr/bin/env python3.4

# -*- encoding: utf-8 -*-

import sqlite3 as dbapi
import os

print ("""\n===========================================================================
============                    *******                     ===============
============              Bienvenido a PassRec              ===============
============    Todas tus contraseñas en un solo archivo!   ===============
============                    *******                     ===============
===========================================================================

""")

def crearDB ():
    """ crea la base de datos con la tabla necesaria para el funcionamiento del programa """
    if not os.path.exists("passrec.db"):
        print ("..... Ahora el programa creará la base de datos ....")
        base_de_datos = dbapi.connect("passrec.db")
        c = base_de_datos.cursor()
        c.execute ("""create table servicios (ident integer primary key autoincrement, nombre text, email text, pass text)""")
        print ("base de datos creada!")
    

def existe ():
    """
    args: none 
    return : int
    
    La función existe, devuelve un entero que es id del ultimo servicio agragado a la base de datos.
    """
    base_de_datos = dbapi.connect ("passrec.db")
    cursor = base_de_datos.cursor()
    cursor.execute( """select ident from servicios where ident = (select max(ident) from servicios) """)    
    ult_registro = cursor.fetchone()
    return ult_registro[0]
    

def agregarServicio ():
    """
    Args: none
    Return : none
    
    La función agregarServicio es la encargada de cargar en la base de datos los servicios que el usuario introduce.
    
    """
    
    repetir = "si"
    while repetir == "si":
        base_de_datos = dbapi.connect ("passrec.db")
        cursor = base_de_datos.cursor()
        try :
            pkey = existe() + 1
        except :
            pkey = 0
        nombre = input ("ingrese el nombre del servicio: ")
        email = input ("ingrese el email asociado al servicio: ")
        paswrd = input ("ingrese la contraseña del servicio: ")
         
        cursor.execute("""insert into servicios values (?, ?, ?, ?)""", (pkey, nombre, email, paswrd))
        base_de_datos.commit()
        repetir = input ("desea seguir agregando servicios? (si / no): ")
        


def buscar_mostrar(nombre=None, email=None):
    """
    Args : str str
    Return : none
    
    La función buscar_mostrar recibe como argumentos dos cadenas, que por defecto estan seteadas con el valor "None"
    Si no se le pasan valores, pregunta al usuario que desea buscar... si se le pasan argumentos busca y muestra los servicios que
    coinciden con lo argumentos dados. 
    
    """
    base_de_datos = dbapi.connect ("passrec.db")
    cursor = base_de_datos.cursor()
    if nombre != None and email == None:
        cursor.execute("""select * from servicios where nombre=? """, (nombre,))
        try :
            existe()
        except:
            print("No se ha encontrado el servicio con ese nombre!")
        for servicio in cursor.fetchall():
            print ("-> Identificador: %s\n->Nombre del servicio: %s\n->Direccion de mail asociada: %s\n->Contraseña: %s\n" %(servicio[0], servicio[1], servicio[2], servicio[3]))
            
    if nombre == None and email != None:
        cursor.execute("""select * from servicios where email=? """, (email,))
        try :
            existe()
        except:
            print("No se ha encontrado el servicio con ese e-mail!")

        for servicio in cursor.fetchall():
            print (servicio)
    if nombre == None and email == None:
        repetir = "si"
        while repetir == "si":
            buscar = int(input ("== Desea buscar por nombre o por email? == \n== Introduzca ( 1 ) para buscar por nombre o ( 2 ) para buscar por email. ==\n=> "))
            if buscar == 1: 
                nombre = input ("Ingrese el nombre del servicio que desea encontrar: ")
                cursor.execute("""select * from servicios where nombre=? """, (nombre,))
                try :
                    existe()
                except:
                    print("No se ha encontrado el servicio con ese nombre!")  
                for servicio in cursor.fetchall():
                    print ("-> Identificador: %s\n->Nombre del servicio: %s\n->Direccion de mail asociada: %s\n->Contraseña: %s\n" %(servicio[0], servicio[1], servicio[2], servicio[3])) 
            if buscar == 2:
                email = input("Ingrese el email a buscar: ")
                cursor.execute("""select * from servicios where email=?""", (email,))
                try :
                    existe()
                except:
                    print("No se ha encontrado el servicio con ese e-mail!")

                for servicio in cursor.fetchall():
                    print ("-> Identificador: %s\n->Nombre del servicio: %s\n->Direccion de mail asociada: %s\n->Contraseña: %s\n" %(servicio[0], servicio[1], servicio[2], servicio[3]))
            repetir = input ("Desea realizar otra busqueda!? (si / no): ")
        
def mostrarTodos():
    """
    Args: none
    REturn: none
    
    mostrarTodos: muestra todos los servicios cargados en la base de datos
    
    """
    base_de_datos = dbapi.connect ("passrec.db")
    cursor = base_de_datos.cursor()
    cursor.execute("""select * from servicios""")
    try:
        existe()
    except :
        print ("*** Parece que no hay nada que mostrar! ***")
    for servicio in cursor.fetchall():
        print ("\n-> Identificador: %s\n-> Nombre del servicio: %s\n-> Direccion de mail asociada: %s\n-> Contraseña: %s\n" %(servicio[0], servicio[1], servicio[2], servicio[3]))
        
def eliminarServicio():
    base_de_datos = dbapi.connect ("passrec.db")
    cursor = base_de_datos.cursor()
    nombre = input ("Que servicio desea eliminar?: ")
    buscar_mostrar(nombre)
    pkey = int(input ("Cual de estos servicios deseas eliminar?\nIntroduzca el Identificador: "))
    cursor.execute ("""delete from servicios where ident=? """, (pkey,))
    base_de_datos.commit()


def menu():
    """
    Args: none
    Reture: none
    
    menu: se encarga de mostrar la interface para el usuario.   
    """
    crearDB()
    print ("Que desea hacer?")
    print ("1 - Agregar un Servicio.\n2 - Buscar\n3 - Eliminar\n4 - Mostrar Todos\n5 - Salir")
    opcion = int(input ("Ingrese la opcion: ")) 
    while opcion != 5:
            if opcion == 1 :
                agregarServicio()
            if opcion == 2 :
                buscar_mostrar()
            if opcion == 3 :
                eliminarServicio()
            if opcion == 4 :
                mostrarTodos()
            print ("1 - Agregar un Servicio.\n2 - Buscar\n3 - Eliminar\n4 - Mostrar Todos\n5 - Salir")
            opcion = int(input ("Ingrese la opcion: "))

menu()

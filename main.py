from datetime import datetime, timedelta
import csv

archivo = "database.csv" #guardamos la ubicacion de la database
campos = ["id", "fecha"] #guardamos los campos del archivo csv

def pedir_fecha(mensaje): #recibe la fecha y verifica su formato
    while True:
        texto = input(mensaje).strip() #estandarizamos el input eliminando espacios innecesarios
        try:
            return datetime.strptime(texto, "%d/%m/%Y") #convertimos el texto a un objeto datetime
        except ValueError:
            print("Formato de fecha inválido. Por favor, use DD/MM/AAAA.")
            return
    
def leer_archivos(): #abrimos el archivo csv y lo leemos, devolviendo una lista de diccionarios con las reservas registradas
    try:
        with open(archivo, "r") as a:
            reader = csv.DictReader(a)
            return list(reader)
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def guardar_archivos(reserva): #recibe una lista de diccionarios con las reservas y las guarda en el archivo
    try:
        with open(archivo, "w", newline="") as a:
            writer = csv.DictWriter(a, fieldnames=campos)
            writer.writeheader()
            writer.writerows(reserva)
        print("Reserva guardada exitosamente.")

    except FileNotFoundError:
        print("El archivo no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def borrar_reserva(id): #borra reservas de un usuario con su id
    dias_reservados = leer_archivos() #buscamos las reservas registradas
    eliminados = [] #lista para fechas que coincidan con el id
    for item in dias_reservados:
        if item['id'] == id:
            eliminados.append(item) #recorremos la lista buscando coincidencias con el id y las guardamos en la lista eliminados
    if eliminados:
        for item in eliminados:
            dias_reservados.remove(item) #removemos los elementos eliminados de la lista original
        guardar_archivos(dias_reservados) #guardamos la lista actualizada
        print("Reserva eliminada exitosamente.")
    else:
        print("No se encontró ninguna reserva con ese ID.")

def auth(id, lista_dias, dias): #autenticacion de datos
    max_dias = 30 #maximo de dias de vacaciones por usuario
    dias_reservados = leer_archivos() #leemos las reservas

    #verificar si estan disponibles los días
    libre = True
    for item in dias_reservados:
        if item['id'] == id: #verificamos con el id cuantas reservas tiene el usuario
            max_dias -= 1 #le restamos de su limite
        if item["fecha"] in lista_dias: #si no esta disponible el dia, cambiamos la variable libre a False
            libre = False

    #verificar si el usuario ha excedido el límite de días reservados
    if dias <= 0:
        print("El número de días pedidos debe ser mayor que cero.")
        return False

    max_dias -= dias #restamos los dias pedidos al limite de dias

    if max_dias <= 0: #si el resultado es menor o igual a cero, el usuario ha excedido su limite de dias
        print("El pedido excede el límite de días reservados.")
        return False

    if libre:
        return True
    else:
        print("Los días seleccionados no están disponibles.")
        return False

def chatbot(): #chatbot que maneja el flujo del programa
    estado = "MENU"
    
    while True: #imprimimos el menu
    
        if estado == "MENU":
            print(">>Bienvenido al sistema de reserva de vacaciones.")
            print()
            print(">>1. Reservar día")
            print(">>2. Ver días reservados")
            print(">>3. Eliminar reserva")
            print(">>4. Salir")
            opcion = input(">>Seleccione una opción: ").strip() #pedimos una opcion al usuario y eliminamos espacios innecesarios

            #cambiamos el estado del chatbot dependiendo de la opcion elegida
            if opcion == "1":
                estado = "RESERVA_ID"
            elif opcion == "2":
                estado = "VER_RESERVAS"
            elif opcion == "3":
                estado = "ELIMINAR_RESERVA"
            elif opcion == "4":
                estado = "SALIR"
            else:
                print("Opción inválida.")
                estado = "MENU"
            continue

        if estado == "RESERVA_ID": #verificamos el ID del usuario
            id = input(">>ingrese su ID: ").strip()

            if not id.isdigit():
                print("ID inválido.")
                estado = "MENU" #en caso de no ser valido volvemos al menu principal
                continue   

            estado = "RESERVA_FECHA_INICIO" #pasamos al siguiente estado
            continue

        if estado == "RESERVA_FECHA_INICIO": #pedimos la fecha de inicio
            incio = pedir_fecha("Ingrese la fecha de inicio (DD/MM/AAAA): ") #mandamos la fecha a la funcion pedir_fecha para verificar su formato

            if not incio: 
                estado = "RESERVA_FECHA_INICIO" #en caso de no ser valido volvemos al menu principal
                continue

            estado = "RESERVA_FECHA_FINAL" #cambiamos al siguiente estado
            continue

        if estado == "RESERVA_FECHA_FINAL": #pedimos la fecha de finalización
            final = pedir_fecha("Ingrese la fecha de finalización (DD/MM/AAAA): ") #mandamos la fecha a la funcion pedir_fecha para verificar su formato

            if not final: 
                estado = "RESERVA_FECHA_FINAL" #en caso de no ser valido volvemos al menu principal
                continue
            else:
                estado = "RESERVA_VALIDAR" #cambiamos al siguiente estado
                continue

        if estado == "RESERVA_VALIDAR": #validamos la reserva
            dias = (final - incio).days #calculamos la diferencia de dias entre la fecha de inicio y final
            lista_dias = [{"id": id, "fecha": (incio + timedelta(days=i)).strftime("%d/%m/%Y")} for i in range(dias + 1)] #creamos una lista con las fechas reservadas

            if auth(id, lista_dias, dias): #autenticamos los datos con la funcion auth
                estado = "RESERVA_GUARDAR" #cambiamos al siguiente estado
                continue
            else:
                print("No se pudo validar la reserva.")
                estado = "MENU" #en caso de no ser valido volvemos al menu principal
                continue

        if estado == "RESERVA_GUARDAR": #guardamos la reserva
            lista = leer_archivos() #leemos el archivo para obtener las reservas registradas
            lista.extend(lista_dias) #le sumamos las reservas del usuario
            guardar_archivos(lista) #guardamos la lista actualizada en el archivo
            print("Reserva guardada exitosamente.")
            estado = "MENU" #volvemos al menu principal
            continue
        
        if estado == "VER_RESERVAS": #mostramos las reservas registradas
            reservas = leer_archivos() #leemos el archivo

            if not reservas: #si no hay reservas registradas
                print("No hay reservas registradas.")
                estado = "MENU" #en caso de no existir reservas volvemos al menu principal
                continue  
            else:
                for reserva in reservas: #recorremos cada reserva y la imprimimos
                    print(f"ID: {reserva['id']}, Fecha: {reserva['fecha']}")
                estado = "MENU" #volvemos al menu principal
                continue

        if estado == "ELIMINAR_RESERVA": #eliminamos las reservas que tengan el id ingresado por el usuario
            id = input("ingrese su id para eliminar su reserva: ").strip() #pedimos id al usuario y eliminamos espacios innecesarios

            if not id.isdigit(): # verificamos que el id sea un número
                print("ID inválido.")
                estado = "MENU" #en caso de no ser valido volvemos al menu principal
                continue

            borrar_reserva(id) #mandamos el id a borrar_reserva y eliminamos la reserva
            print("Reserva eliminada exitosamente.")
            estado = "MENU" #volvemos al menu principal
            continue
            
        if estado == "SALIR": #salimos del programa
            print("Gracias por usar el sistema de reservas. ¡Hasta luego!")
            break
        
            

chatbot()
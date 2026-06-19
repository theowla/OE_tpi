from datetime import datetime, timedelta
import csv

archivo = "database.csv"
campos = ["id", "fecha"]
def fecha(mensaje):
    while True:
        try:
            fecha = input(mensaje)
            return datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            print("Formato de fecha inválido. Por favor, use DD/MM/AAAA.")
            return
    
def leer_archivos():
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

def guardar_archivos(reserva):
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

def borrar_reserva(id):
    dias_reservados = leer_archivos()
    eliminados = []
    for item in dias_reservados:
        if item['id'] == id:
            eliminados.append(item)
    if eliminados:
        for item in eliminados:
            dias_reservados.remove(item)
        guardar_archivos(dias_reservados)
    else:
        print("No se encontró ninguna reserva con ese ID.")

def chatbot():
    #menu de opciones
    print("Bienvenido al sistema de reservas.")
    print("1. Reservar un día")
    print("2. Ver días reservados")
    print("3. Eliminar tu reserva")
    print("4. Salir")

    #input de usuario
    opcion = input("Selecciones una opción: ")
    if opcion.isdigit():
        opcion = int(opcion)
        #elección de opciones
        if opcion == 1:
            #reservar un día
                id = input("Ingrese su id: ")
                inicio = fecha("Ingrese la fecha de inicio (DD/MM/AAAA): ")
                final = fecha("Ingrese la fecha de final (DD/MM/AAAA): ")
                dias_disponibles = 15
                dias = (final - inicio).days

                lista_dias = [ {"id": id, "fecha": (inicio + timedelta(days=i)).strftime("%d/%m/%Y")}
                for i in range(dias + 1)
                ]
                if auth(id, lista_dias, dias):
                    lista = leer_archivos()
                    lista.extend(lista_dias)
                    guardar_archivos(lista)
        elif opcion == 2:
            #ver días reservados
            reservas = leer_archivos()  
            for reserva in reservas:
                print(f"ID: {reserva['id']}, Fecha: {reserva['fecha']}")
            return
        elif opcion == 3:
            id = input("ingrese su id para eliminar su reserva: ")
            if id.isdigit():
                #eliminar reserva
                borrar_reserva(id)
            else:
                print("ID inválido.")
                return
        elif opcion == 4:
            print("Gracias por usar el sistema de reservas. ¡Hasta luego!")
            return
    else:
        print("Opción inválida.")
        return
def auth(id, lista_dias, dias):
    max_dias = 30
    dias_reservados = leer_archivos()

    #verificar si estan disponibles los días
    libre = True
    for item in dias_reservados:
        if item['id'] == id:
            max_dias -= 1
        if item["fecha"] in lista_dias:
            libre = False

    #verificar si el usuario ha excedido el límite de días reservados
    if dias <= 0:
        print("El número de días pedidos debe ser mayor que cero.")
        return False
    max_dias -= dias
    if max_dias <= 0:
        print("El pedido excede el límite de días reservados.")
        return False
    if libre:
        return True
    else:
        print("Los días seleccionados no están disponibles.")
        return False

chatbot()
# Sistema de reserva de vacaciones.
Es un chatbot que automatiza la gestion de solicitudes de vacaciones de empleados.

## Requisitos
-Python 3.8 o superior

## Instalacion y ejecucion
```bash
git clone https://github.com/theowla/OE_tpi.git
cd OE_tpi
python main.py
```
## Estructura del proyecto
```
.
├── main.py          # Código fuente del chatbot
├── database.csv     # Base de datos de reservas (id, fecha)
└── README.md
```
## Uso
Al ejecutar el programa aparece el siguiente menu:
```
>>Bienvenido al sistema de reserva de vacaciones.
 
>>1. Reservar día
>>2. Ver días reservados
>>3. Eliminar reserva
>>4. Salir
```
-**opcion 1:** solicita id y fechas(inicio y fin) al usuario. Valida que haya saldo disponible (Max 30 dias) y disponibilidad de esas fechas.

-**opcion 2:** Imprime todas las reservas registradas.

-**opcion 3:** Elimina todas las reservas del id que pida el usuario.

-**opcion 4:** Cierra el programa

## Reglas del programa
- Hay un maximo de 30 dias de vacaciones por usuario.
- No se pueden reservar fechas ocupadas.
- Las fechas deben ingresarse en formato DD/MM/AAAA.
- El periodo minimo de vacaciones es de 1 dia.

## Flujo de estados
```
MENU → RESERVA_ID → RESERVA_FECHA_INICIO → RESERVA_FECHA_FINAL → RESERVA_VALIDAR → RESERVA_GUARDAR → MENU
MENU → VER_RESERVAS → MENU
MENU → ELIMINAR_RESERVA → MENU
MENU → SALIR
```


import pandas as pd
import datetime as dt
from tabulate import tabulate  # type: ignore

fecha_hoy = dt.date.today()

salas = {1:["ITALIA", 30],2:["FRANCIA",50]}
contador_salas = 3

folios_eventos = [1,2]
eventos = {"sala" : [1,2],
           "cliente" : [1,1],
           "evento" : ["CUMPLEAÑOS SAUL","CONCIERTO"],
           "turno" : ["NOCTURNO","MATUTINO"],
           "fecha" : ["30/09/2025","30/09/2025"]
           }
contador_eventos = 3

claves_clientes = [1]
clientes = {"apellidos" : ["CEDILLO"],
            "nombres" : ["JOSUE"],
            }
contador_clientes = 2

print("*"*51)
print("*Bienvenido al sistema de reservacion de eventos*")
print("*"*51)

while True:
    print("\n****Menu**")
    print("1.Registrar evento")
    print("2.Editar nombre del evento")
    print("3.Consultar reservaciones")
    print("4.Registrar cliente")
    print("5.Registrar sala")
    print("6.Salir")
    print("*"*30)
    
    try:
        opcion = int(input("Ingrese una opcion: "))
    except ValueError:
        print("Favor de digitar un numero valido\n")
        continue
    
    match opcion:
        case 1:
            print("\nRegristrar evento")            
            df_clientes = pd.DataFrame(clientes)
            df_clientes.index = claves_clientes
            df_clientes.index.name = "Id_cte"
            df_clientes = df_clientes.sort_values(by="apellidos")
            
            while True:
                print("\n*Clientes registrados*")
                print(df_clientes)
                print("*"*30)
                salida = input("Escriba X si quiere regresar al menu principal: ")
                if salida.upper() == "X":
                    break
                
                try:
                    clave_cliente_elegida = int(input("Ingresa tu clave de cliente: "))
                    if clave_cliente_elegida not in claves_clientes:
                        print("El cliente no existe\n")
                        continue
                    else:
                        while True:     
                            fecha_elegida = input("Ingrese la fecha del evento (dd/mm/aaaa): ")
                            try:
                                fecha_evento = dt.datetime.strptime(fecha_elegida, "%d/%m/%Y").date()
                                
                                
                            except ValueError:
                                print("Favor de digitar una fecha valida\n")
                                continue

                            if (fecha_evento - fecha_hoy).days < 2:
                                print("La fecha debe ser al menos dos días después de la fecha actual\n")
                                continue
                            break
                        
                        print("\n")
                        eventos_df = pd.DataFrame(eventos)
                        eventos_df.index = folios_eventos
                        eventos_df.index.name = "Folio"
                        filtro_fecha = eventos_df["fecha"] == fecha_elegida
                        eventos_fecha = eventos_df[filtro_fecha]
                        
                        salas_turnos_disponibles = {}
                        for sala_id, sala_info in salas.items():
                            nombre_sala = sala_info[0]
                            capacidad_sala = sala_info[1]
                            
                            turnos_ocupados = []
                            for _, row in eventos_fecha.iterrows():
                                if row["sala"] == sala_id:
                                    turnos_ocupados.append(row["turno"])
                            
                            turnos_disponibles = [turno for turno in ["MATUTINO", "VESPERTINO", "NOCTURNO"] if turno not in turnos_ocupados]
                            
                            if fecha_elegida not in salas_turnos_disponibles:
                                salas_turnos_disponibles[fecha_elegida] = {}
                            salas_turnos_disponibles[fecha_elegida][nombre_sala] = [capacidad_sala, turnos_disponibles]

                        print("Salas disponibles para la fecha seleccionada")
                        for sala_nombre, info in salas_turnos_disponibles[fecha_elegida].items():
                            print(f"Sala: {sala_nombre}, Capacidad: {info[0]}, Turnos disponibles: {', '.join(info[1])}")
                        print("*"*55)
                        
                        while True:
                            sala_elegida = input("Ingrese el nombre de la sala: ")
                            if not sala_elegida:
                                print("El nombre de la sala no puede estar vacio\n")
                                continue
                            
                            sala_encontrada = False
                            for sala_id, sala_info in salas.items():
                                if sala_info[0] == sala_elegida.upper():
                                    sala_encontrada = True
                                    sala_id_elegida = sala_id
                                    break
                            
                            if not sala_encontrada:
                                print("La sala no existe\n")
                                continue
                            
                            while True:
                                try:
                                    cupo_evento = int(input("Ingrese el cupo del evento: "))
                                    if cupo_evento <= 0:
                                        print("El cupo del evento debe ser mayor a 0\n")
                                        continue
                                except ValueError:
                                    print("Favor de digitar un numero valido\n")
                                    continue
                                
                                if cupo_evento > salas[sala_id_elegida][1]:
                                    print(f"El cupo del evento excede la capacidad de la sala\n")
                                    continue
                                break
                            break

                        while True:
                            turno_elegido = input("Ingrese el turno (MATUTINO, VESPERTINO, NOCTURNO): ")
                            if turno_elegido.upper() not in ["MATUTINO", "VESPERTINO", "NOCTURNO"]:
                                print("Turno no valido\n")
                                continue
                            
                            turno_ocupado = False
                            for turno_disponible in salas_turnos_disponibles[fecha_elegida][sala_elegida.upper()][1]:
                                if turno_elegido.upper() == turno_disponible.upper():
                                    break
                                else:
                                    turno_ocupado = True
                            
                            if turno_ocupado:
                                print("Este turno ya está ocupado para la sala y fecha seleccionadas. Por favor, elija otro turno.\n")
                                continue
                            break
                        
                        while True:
                            nombre_evento = input("Ingrese el nombre del evento: ")
                            if not nombre_evento:
                                print("El nombre del evento no puede estar vacio\n") 
                                continue
                            if nombre_evento.isspace():
                                print("El nombre del evento no puede consistir solo en espacios en blanco\n")
                                continue
                            break

                        folios_eventos.append(contador_eventos)
                        eventos["sala"].append(sala_id_elegida)
                        eventos["cliente"].append(clave_cliente_elegida)
                        eventos["evento"].append(nombre_evento.upper())
                        eventos["turno"].append(turno_elegido.upper())
                        eventos["fecha"].append(fecha_elegida)
                        contador_eventos += 1
                        print("Evento registrado con exito")
                        
                        break      
                except ValueError:
                    print("Favor de digitar un numero valido\n")
                    continue
        
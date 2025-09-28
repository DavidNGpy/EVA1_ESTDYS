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
    print("\n*******Menu*******")
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

                        print("*Salas disponibles para la fecha seleccionada*")
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
        
        case 2:
            print("\nEditar nombre del evento")
            while True:
                fecha_inicio = input("Ingrese desde que fecha consultar los eventos (dd/mm/aaaa): ")
                try:
                    fecha_inicio = dt.datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
                    break
                except ValueError:
                    print("Favor de digitar una fecha valida\n")
                    continue

            while True:
                fecha_fin = input("Ingrese hasta que fecha consultar los eventos (dd/mm/aaaa): ")
                try:
                    fecha_fin = dt.datetime.strptime(fecha_fin, "%d/%m/%Y").date()
                    if fecha_fin < fecha_inicio:
                        print("La fecha final no puede menor a la fecha inicial\n")
                        continue
                    break
                except ValueError:
                    print("Favor de digitar una fecha valida\n")
                    continue

            eventos_df = pd.DataFrame(eventos)
            eventos_df.index = folios_eventos
            eventos_df.index.name = "Folio"
            
            eventos_df["fecha_dt"] = pd.to_datetime(eventos_df["fecha"], format="%d/%m/%Y").dt.date
            
            filtro_rango_fechas = (eventos_df["fecha_dt"] >= fecha_inicio) & (eventos_df["fecha_dt"] <= fecha_fin)
            eventos_en_rango = eventos_df[filtro_rango_fechas].drop(columns=["fecha_dt"])

            if eventos_en_rango.empty:
                print(f"\nNo hay eventos registrados entre {fecha_inicio} y {fecha_fin}\n")
            else:
                print(f"\n*Eventos registrados entre {fecha_inicio} y {fecha_fin}*")
                print(eventos_en_rango)
                print("*"*30)

            while True:
                salida = input("Escriba X si quiere regresar al menu principal: ")
                if salida.upper() == "X":
                    break
                try:
                    folio_evento_elegido = int(input("Ingrese el folio del evento a editar: "))
                    if folio_evento_elegido not in folios_eventos:
                        print("El folio del evento no existe\n")
                        print(eventos_en_rango)
                        continue
                    else:
                        nuevo_nombre_evento = input("Ingrese el nuevo nombre del evento: ")
                        if not nuevo_nombre_evento:
                            print("El nombre del evento no puede estar vacio\n")
                            continue
                        if nuevo_nombre_evento.isspace():
                            print("El nombre del evento no puede consistir solo en espacios en blanco\n")
                            continue
                        
                        indice_evento = folios_eventos.index(folio_evento_elegido)
                        eventos["evento"][indice_evento] = nuevo_nombre_evento.upper()
                        print("Nombre del evento editado con exito")
                        break
                except ValueError:
                    print("Favor de digitar un numero valido\n")
                    continue
                
        case 3:
            while True:
                fecha_consulta = input("Ingrese la fecha a consultar (dd/mm/aaaa): ")
                try:
                    fecha_consulta_dt = dt.datetime.strptime(fecha_consulta, "%d/%m/%Y").date()
                    break
                except ValueError:
                    print("Favor de digitar una fecha valida\n")
                continue
    
            eventos_df = pd.DataFrame(eventos)
            eventos_df.index = folios_eventos
            eventos_df.index.name = "Folio"

            filtro_fecha_consulta = eventos_df["fecha"] == fecha_consulta

            if eventos_df[filtro_fecha_consulta].empty:
                    print(f"\nNo hay eventos registrados para la fecha {fecha_consulta}\n")
            else:
                    print(f"\n*Eventos registrados para el {fecha_consulta}*")
        
            df_clientes = pd.DataFrame(clientes)
            df_clientes.index = claves_clientes
            df_clientes.index.name = "CLIENTES"
        
            filas_tabla = []

            for folio, evento_data in eventos_df[filtro_fecha_consulta].iterrows():
                sala_id = evento_data["sala"]
                cliente_id = evento_data["cliente"]
                nombre_evento = evento_data["evento"]
                turno = evento_data["turno"]

                nombre_sala = salas[sala_id][0]
                nombre_cliente = df_clientes.loc[cliente_id, "nombres"]
                apellido_cliente = df_clientes.loc[cliente_id, "apellidos"]

                filas_tabla.append([nombre_sala, f"{nombre_cliente} {apellido_cliente}", nombre_evento, turno])
                   
            headers = ["SALA","CLIENTE","EVENTO","TURNO"]

            tabla = tabulate(filas_tabla, headers, tablefmt="plain")

            print("*" * 70)
            print(f"\tREPORTE DE RESERVACIONES PARA EL DÍA {fecha_consulta}\t**")
            print("*" * 70)
            print(tabla)
            print("*" * 70)
            print("\t\t\tFIN DEL REPORTE\t\t\t**")    
            print("*" * 70)

            continue
        
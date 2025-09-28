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


# Hoja_5.py
# UVG - Algoritmos y Estructuras de Datos
# Julio Merida  15242   //  Raul de Leon  15112
# 31/08/2016

# Librerias de Simpy y para uso de random
import simpy
import random
import math 

# Variables a usar

global memoria
memoria = 100 #espacio de memoria RAM
tiempoT = 0.0 #contador para el tiempo de los procesos
promedio = 0.0 #tiempo medio de los procesos
capacidad = 10
tiempo = 1
semilla = 127 #semilla para el numero al azar
cant_procesos = 25 #cantidad de procesos que se crean
max_io = 3 #tiempo maximo que pueden tardar las operaciones
cant_inst = 10 #cantidad maxima que pueden tener los procesos

lista = []


# Funcion para definir un proceso
def ProcesoIndividual(env, nombre, unidades, ram, IO, mem, ins):
	init = int(env.now)
	print('Proceso %s creado en %s unidades' %(nombre,init))
	global tiempoT, tiempo, capacidad

	with ram.get(ins) as req:
	
		yield req
		
		initready = int(env.now)
		print('Proceso %s esta listo, en %s unidades' %(nombre,initready))


		while(ins >0):
			with unidades.request() as req2:
				yield req2
				initprocesos = int(env.now)
				print('Proceso %s ha ejecutado 3 instrucciones, %s unidades' %(nombre,initprocesos))
				ins -= 3
				ram.put(3)

				if(random.randint(1,2)==1):
					with IO.request() as req3:
					
						yield req3
						initIO = int(env.now)
						print('Proceso %s ingreso a I/O, %s unidades' % (nombre,initIO))
						tiempoesperaIO = random.randint(1,max_io)
						yield env.timeout(tiempoesperaIO)
						salidaIO = int(env.now)
						tiempo = salidaIO - init
						lista.append(salidaIO)
						print('Proceso %s termino I/O, %s unidades' % (nombre,salidaIO))

						
						
		yield env.timeout(tiempo)
		
		exitprocesos = int(env.now)
		
		print('Proceso %s finalizado, %s unidades' %(nombre,exitprocesos))
		
		tiempoT = tiempoT + exitprocesos - init


# Funcion para iniciar el proceso
def Procesar(env, cantidad, capacidad, unidades,IO,ram):

	global cant_inst, memoria
	
	for i in range(cantidad+1):
		memoria = random.randint(1,capacidad)
		instruc = random.randint(1,cant_inst)
		nuevo_proceso = ProcesoIndividual(env,str(i),unidades,ram,IO,memoria,instruc)
		env.process(nuevo_proceso)
		temptime = random.expovariate(1.0/capacidad)
		
		yield env.timeout(temptime)
	

# Ejecucion delas instrucciones
env = simpy.Environment()
#Generacion de random usando una semilla predeterminada
random.seed(semilla)
#Implementacion de biblioteca Simpy para iniciar simulacion
procesador = simpy.Resource(env, capacity=1)
ram_TOTAL = simpy.Container(env, capacity=memoria, init = memoria)
IO = simpy.Resource(env, capacity=1)
env.process(Procesar(env,cant_procesos,capacidad,procesador,IO,ram_TOTAL))

# Se corre la simulacion
env.run()
# Operacion para hallar promedio
promedio = tiempoT/cant_procesos
print('Promedio para todos los proceos es de %s' % (promedio))

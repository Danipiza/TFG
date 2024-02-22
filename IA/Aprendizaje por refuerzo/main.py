import numpy as np

# Seleciona una accion basada en epsilon-greedy
def seleciona_accion(estado):
    if np.random.uniform(0, 1) < epsilon: return np.random.choice(len(acciones))
    else: return np.argmax(Q_table[estado[0], estado[1]])

# Actualiza la tabla Q
def actualiza_Q_table(estado, accion, recompensa, sig_estado):
    best_next_action = np.argmax(Q_table[sig_estado[0], sig_estado[1]])
    Q_table[estado[0], estado[1], accion] += alpha * (recompensa + gamma * Q_table[sig_estado[0], sig_estado[1], best_next_action] - Q_table[estado[0], estado[1], accion])

# Dentro del tablero, y no es pared
def accion_valida(estado, accion):
    sig_estado = (estado[0] + accion[0], estado[1] + accion[1])
    return 0<=sig_estado[0]<matriz.shape[0] and 0<=sig_estado[1]<matriz.shape[1] and matriz[sig_estado[0], sig_estado[1]]==0


def entrenamiento(episodios):
	
	for ep in range(episodios):
		estado = (0, 0)
		# Hasta que el agente llegue al objetivo
		while estado != (4, 4):  
			accion = seleciona_accion(estado)
			if accion_valida(estado, acciones[accion]):
				sig_estado = (estado[0] + acciones[accion][0], estado[1] + acciones[accion][1])
				if matriz[sig_estado[0], sig_estado[1]] == 1: 
					recompensa = recompensas['pared']
				elif sig_estado == (4, 4): 
					recompensa = recompensas['destino']
				else: 
					recompensa = recompensas['otro']
				actualiza_Q_table(estado, accion, recompensa, sig_estado)
				estado = sig_estado

def ejecuta():

	entrenamiento(1000)
	print("Ha terminado el entrenamiento")

	# Evaluación del Agente
	
	estado = (0, 0) # Numero aleatorio
	while estado != (4, 4):
		accion = np.argmax(Q_table[estado[0], estado[1]])
		if accion_valida(estado, acciones[accion]):
			estado = (estado[0] + acciones[accion][0], estado[1] + acciones[accion][1])
			print(f"Siguiente accion: {acciones[accion]}, Siguiente estado: {estado}")
		else:
			print("No puede avanzar")
			break


# Definir el laberinto 0: vacio, 1: pared
matriz = np.array([	[0, 1, 0, 0, 0],
					[0, 1, 0, 1, 0],
					[0, 0, 0, 1, 0],
					[0, 1, 1, 1, 0],
					[0, 0, 0, 1, 0]])

# Definir acciones (arriba, abajo, izquierda, derecha)
acciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Definir recompensas
recompensas = {
    'destino': 100,
    'pared': -10,
    'otro': -1}

# Parametros de aprendizaje
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Factor de exploración

# Inicializar la Q table
Q_table = np.zeros((matriz.shape[0], matriz.shape[1], len(acciones)))

ejecuta()

# =============================================================================
# Archivo: entrega1_por_ia.py
# Materia: Inteligencia Artificial
# =============================================================================

from simpleai.search import SearchProblem, astar

class RoverProblem(SearchProblem):
    def __init__(self, rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
        # Estado inicial inmutable (tuplas y frozensets)
        # Componentes del estado:
        # 0: pos (fila, columna) del rover
        # 1: bateria actual (entero de 0 a 20)
        # 2: taladro equipado (None, "termico" o "percusion")
        # 3: carga actual en la bodega (frozenset de strings: "ignea" y/o "sedimentaria")
        # 4: posiciones de muestras igneas restantes (frozenset)
        # 5: posiciones de muestras sedimentarias restantes (frozenset)
        self.initial_state = (
            rover_inicio,
            bateria_inicial,
            None,
            frozenset(),
            frozenset(muestras_igneas),
            frozenset(muestras_sedimentarias)
        )
        self.zonas_sombra = set(zonas_sombra)

    def actions(self, state):
        pos, bateria, taladro, carga, igneas, sedim = state
        f, c = pos
        list_actions = []

        # --- ACCIÓN: RECARGAR ---
        # No se puede recargar en zonas de sombra ni si ya está al tope (20)
        if pos not in self.zonas_sombra and bateria < 20:
            list_actions.append(("recargar", None))

        # --- ACCIÓN: EQUIPAR ---
        # El test valida los strings estrictamente sin acento: "termico" y "percusion"
        if taladro != "termico" and bateria >= 1:
            list_actions.append(("equipar", "termico"))
        if taladro != "percusion" and bateria >= 1:
            list_actions.append(("equipar", "percusion"))

        # --- ACCIÓN: RECOLECTAR ---
        # Requiere espacio en bodega (< 2), taladro correcto y tener al menos 3 de batería
        if len(carga) < 2 and bateria >= 3:
            if pos in igneas and taladro == "termico":
                list_actions.append(("recolectar", "ignea"))
            if pos in sedim and taladro == "percusion":
                list_actions.append(("recolectar", "sedimentaria"))

        # --- ACCIÓN: DEPOSITAR ---
        # Si tiene carga, se puede depositar si la bodega está llena (2)
        # O si ya no quedan más muestras en todo el mapa (es la última tanda)
        if len(carga) > 0 and bateria >= 1:
            muestras_restantes_mapa = len(igneas) + len(sedim)
            if len(carga) == 2 or muestras_restantes_mapa == 0:
                list_actions.append(("depositar", None))

        # --- ACCIÓN: MOVERSE (1 celda adyacente) ---
        if bateria >= 1:
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
            for df, dc in direcciones:
                nueva_pos = (f + df, c + dc)
                list_actions.append(("moverse", nueva_pos))

        # --- ACCIÓN: SOBREMARCHA (2 celdas en línea recta) ---
        if bateria >= 4:
            saltos = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for df, dc in saltos:
                nueva_pos = (f + df, c + dc)
                list_actions.append(("sobremarcha", nueva_pos))

        return list_actions

    def result(self, state, action):
        pos, bateria, taladro, carga, igneas, sedim = state
        tipo, param = action

        nueva_pos = pos
        nueva_bateria = bateria
        nuevo_taladro = taladro
        nueva_carga = carga
        nuevas_igneas = igneas
        nuevas_sedim = sedim

        if tipo == "moverse":
            nueva_pos = param
            nueva_bateria -= 1

        elif tipo == "sobremarcha":
            nueva_pos = param
            nueva_bateria -= 4

        elif tipo == "equipar":
            nuevo_taladro = param
            nueva_bateria -= 1

        elif tipo == "recolectar":
            nueva_bateria -= 3
            # Convertimos a lista para agregar la muestra y volvemos a frozenset
            lista_carga = list(carga)
            lista_carga.append(param)
            nueva_carga = frozenset(lista_carga)

            # Sacamos la muestra recolectada del mapa
            if param == "ignea":
                nuevas_igneas = igneas - {pos}
            elif param == "sedimentaria":
                nuevas_sedim = sedim - {pos}

        elif tipo == "depositar":
            # Consume 1 de batería por cada muestra entregada
            nueva_bateria -= len(carga)
            nueva_carga = frozenset()  # Se vacía por completo la bodega

        elif tipo == "recargar":
            # Restaura 10 unidades de batería sin pasarse del máximo de 20
            nueva_bateria = min(20, bateria + 10)

        return (nueva_pos, nueva_bateria, nuevo_taladro, nueva_carga, nuevas_igneas, nuevas_sedim)

    def cost(self, state, action, state2):
        # El costo representa el tiempo en minutos que toma la acción
        tipo, param = action
        if tipo == "moverse":
            return 1
        elif tipo == "sobremarcha":
            return 1
        elif tipo == "equipar":
            return 3
        elif tipo == "recolectar":
            return 2
        elif tipo == "depositar":
            # El test calcula el tiempo multiplicando por la carga antes de vaciar:
            # total_cost += times["depositar"] * load -> 1 * len(carga)
            return len(state[3])
        elif tipo == "recargar":
            return 4
        return 0

    def is_goal(self, state):
        pos, bateria, taladro, carga, igneas, sedim = state
        # Se cumple la meta si no quedan muestras en el mapa, ni en el rover, y sigue con vida (> 0 bateria)
        return len(igneas) == 0 and len(sedim) == 0 and len(carga) == 0 and bateria > 0

    def heuristic(self, state):
        pos, bateria, taladro, carga, igneas, sedim = state
        
        # Heurística admisible (nunca sobreestima el costo real):
        # Cada roca en el suelo costará al menos: 2m (recolectar) + 1m (depositar) = 3 minutos.
        # Cada roca ya cargada costará al menos: 1m (depositar).
        # Ignoramos movimientos y cambios de taladro para asegurar optimismo estricto.
        rocas_mapa = len(igneas) + len(sedim)
        rocas_carga = len(carga)
        
        return (rocas_mapa * 3) + (rocas_carga * 1)


def planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
    problema = RoverProblem(
        rover_inicio, 
        bateria_inicial, 
        zonas_sombra, 
        muestras_igneas, 
        muestras_sedimentarias
    )
    
    # Resolvemos usando A* (astar) con búsqueda en grafo para evitar ciclos repetidos
    resultado = astar(problema, graph_search=True)
    
    if resultado:
        plan = []
        for accion, nuevo_estado in resultado.path():
            if accion is not None:
                plan.append(accion)
        return plan
    else:
        return []
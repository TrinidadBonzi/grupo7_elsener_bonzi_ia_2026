from simpleai.search import SearchProblem, astar

class RoverProblem(SearchProblem):
    def __init__(self, rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
        self.rover_inicio = rover_inicio
        self.bateria_inicial = bateria_inicial
        self.zonas_sombra = set(zonas_sombra)
        self.muestras_igneas = set(muestras_igneas)
        self.muestras_sedimentarias = set(muestras_sedimentarias)

        # Estado inicial: (pos, batería, taladro, carga, igneas, sedimentarias)
        initial_state = (
            rover_inicio,
            bateria_inicial,
            None,
            0,  # carga como número
            frozenset(self.muestras_igneas),
            frozenset(self.muestras_sedimentarias),
        )
        super().__init__(initial_state)

    def actions(self, state):
        pos, bateria, taladro, carga, igneas, sedimentarias = state
        acciones = []

        # Movimiento normal
        if bateria >= 1:
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nueva = (pos[0]+dx, pos[1]+dy)
                acciones.append(("moverse", nueva))

        # Sobremarcha
        if bateria >= 4:
            for dx, dy in [(2,0), (-2,0), (0,2), (0,-2)]:
                nueva = (pos[0]+dx, pos[1]+dy)
                acciones.append(("sobremarcha", nueva))

        # Equipar taladro
        if bateria >= 1:
            if taladro != "termico":
                acciones.append(("equipar", "termico"))
            if taladro != "percusion":
                acciones.append(("equipar", "percusion"))

        # Recolectar
        if bateria >= 3 and carga < 2:
            if pos in igneas and taladro == "termico":
                acciones.append(("recolectar", "ignea"))
            if pos in sedimentarias and taladro == "percusion":
                acciones.append(("recolectar", "sedimentaria"))

        # Depositar
        if carga > 0:
            acciones.append(("depositar", None))

        # Recargar (solo si batería baja)
        if pos not in self.zonas_sombra and bateria <= 15:
            acciones.append(("recargar", None))

        return acciones

    def result(self, state, action):
        pos, bateria, taladro, carga, igneas, sedimentarias = state
        tipo, param = action

        if tipo == "moverse":
            return (param, bateria-1, taladro, carga, igneas, sedimentarias)
        elif tipo == "sobremarcha":
            return (param, bateria-4, taladro, carga, igneas, sedimentarias)
        elif tipo == "equipar":
            return (pos, bateria-1, param, carga, igneas, sedimentarias)
        elif tipo == "recolectar":
            if param == "ignea":
                nuevas = frozenset(igneas - {pos})
                return (pos, bateria-3, taladro, carga+1, nuevas, sedimentarias)
            else:
                nuevas = frozenset(sedimentarias - {pos})
                return (pos, bateria-3, taladro, carga+1, igneas, nuevas)
        elif tipo == "depositar":
            return (pos, bateria-1, taladro, 0, igneas, sedimentarias)
        elif tipo == "recargar":
            return (pos, min(20, bateria+10), taladro, carga, igneas, sedimentarias)

    def cost(self, state1, action, state2):
        tipo, _ = action
        if tipo == "moverse": return 1
        if tipo == "sobremarcha": return 1
        if tipo == "equipar": return 3
        if tipo == "recolectar": return 2
        if tipo == "depositar": return state1[3]  # 1 min por muestra
        if tipo == "recargar": return 4

    def is_goal(self, state):
        _, _, _, carga, igneas, sedimentarias = state
        return carga == 0 and not igneas and not sedimentarias

    def heuristic(self, state):
        pos, _, _, carga, igneas, sedimentarias = state
        muestras = list(igneas) + list(sedimentarias)
        if not muestras and carga == 0:
            return 0
        distancias = [abs(pos[0]-m[0]) + abs(pos[1]-m[1]) for m in muestras]
        return (min(distancias) if distancias else 0) + len(muestras) + carga

def planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
    problema = RoverProblem(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias)
    resultado = astar(problema)
    return [accion for accion, _ in resultado.path()[1:]]
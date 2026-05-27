from simpleai.search import astar, SearchProblem

class RoverProblem (SearchProblem):
    def __init__(
        self,
        rover_inicio,
        bateria_inicial,
        zonas_sombra,
        muestras_igneas,
        muestras_sedimentarias,
    ):
        self.zonas_sombra = zonas_sombra
        self.bateria_maxima = 20
        self.capacidad_maxima = 2
        
        taladro_equipado = None
        carga_actual = 0
        
        todas = (
            [rover_inicio]
            + list(zonas_sombra)
            + list(muestras_igneas)
            + list(muestras_sedimentarias)
        )

        self.min_x = min(x for x, y in todas) 
        self.max_x = max(x for x, y in todas) 

        self.min_y = min(y for x, y in todas) 
        self.max_y = max(y for x, y in todas) 
        
        inicial = (rover_inicio, bateria_inicial, taladro_equipado, carga_actual, tuple(muestras_igneas), tuple(muestras_sedimentarias))
        super(RoverProblem, self).__init__(inicial)
        
        
    def is_goal(self, state):
        posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria = state
        return (len(mIgnea)== 0 and len(mSedimentaria)== 0 and carga == 0)
    
    def actions(self, state):
        posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria = state
        
        acciones = []
        
        x, y = posicionRover
        
        movimientos = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]        
        
        if bateriaInicial > 1:
            for destino in movimientos:
                nx, ny = destino
                if self.min_x <= nx <= self.max_x and self.min_y <= ny <= self.max_y:
                    acciones.append(("moverse", destino))
                
                
        sobremarchas = [
            (x - 2, y),
            (x + 2, y),
            (x, y - 2),
            (x, y + 2),
        ]
        
        if bateriaInicial > 4:
            for destino in sobremarchas:
                nx, ny = destino
                if self.min_x <= nx <= self.max_x and self.min_y <= ny <= self.max_y:
                    acciones.append(("sobremarcha", destino))
         
        if bateriaInicial > 1:
            if taladro != "termico" and mIgnea:
                acciones.append(("equipar", "termico"))
            if taladro != "percusion" and mSedimentaria:
                acciones.append(("equipar", "percusion"))
                
        if carga < self.capacidad_maxima and bateriaInicial > 3:
            if posicionRover in mIgnea and taladro == "termico":
                acciones.append(("recolectar", "ignea"))
                
            if posicionRover in mSedimentaria and taladro == "percusion":
                acciones.append(("recolectar", "sedimentaria"))
                
        if carga > 0 and bateriaInicial > 1:  # necesita al menos 2 para no quedar en 0
            if carga == self.capacidad_maxima:
                acciones.append(("depositar", None))
            elif carga == 1 and (len(mIgnea) + len(mSedimentaria) == 0):
                acciones.append(("depositar", None))

        if bateriaInicial < self.bateria_maxima and posicionRover not in self.zonas_sombra:
            acciones.append(("recargar", None))
          
        return acciones
    
    def result(self, state, action):
        posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria = state
        accion, parametro = action 
        
        if accion == "moverse":
            posicionRover = parametro
            bateriaInicial -= 1
        
        elif accion == "sobremarcha":
            posicionRover = parametro
            bateriaInicial -= 4
            
        elif accion == "equipar":
            taladro = parametro
            bateriaInicial -= 1
        
        elif accion == "recolectar":
            carga += 1
            bateriaInicial -= 3
            
            igneas = list(mIgnea)
            sedimentarias = list(mSedimentaria)
            
            if parametro == "ignea":
                igneas.remove(posicionRover)
            elif parametro == "sedimentaria":
                sedimentarias.remove(posicionRover)
            
            mIgnea = tuple(sorted(igneas))
            mSedimentaria = tuple(sorted(sedimentarias))
        
        elif accion == "depositar":
            if bateriaInicial <= 1:
                return state  
            bateriaInicial -= 1  
            carga = 0
           
        elif accion == "recargar":
            bateriaInicial += 10
            
            if bateriaInicial > self.bateria_maxima:
                bateriaInicial = self.bateria_maxima
        
        return (posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria)
    
    def cost(self, state, action, state2):
        posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria = state
        accion, parametro = action
        
        if accion == "moverse":
            return 1
        elif accion == "sobremarcha":
            return 1
        elif accion == "equipar":
            return 3
        elif accion == "recolectar":
            return 2
        elif accion == "depositar":
            return 1  # tiempo fijo

        elif accion == "recargar":
            return 4
                    
def heuristic(self, state):
       posicionRover, _, _, _, mIgnea, mSedimentaria = state
       muestras = list(mIgnea) + list(mSedimentaria)
       if not muestras:
           return 0
       x, y = posicionRover
       dist_min = min(abs(mx - x) + abs(my - y) for mx, my in muestras)
       return dist_min + len(muestras) * 2
        
        
def planear_rover(
    rover_inicio,
    bateria_inicial,
    zonas_sombra,
    muestras_igneas,
    muestras_sedimentarias, 
):
    problema = RoverProblem(
        rover_inicio,
        bateria_inicial,
        zonas_sombra,
        muestras_igneas,
        muestras_sedimentarias, 
    )
    
    resultado = astar(problema, graph_search=True)

    acciones = []
    
    for accion, estado in resultado.path():
        if accion is not None:
            acciones.append(accion)
    
    return acciones
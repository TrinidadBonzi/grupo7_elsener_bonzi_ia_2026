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
        
        inicial = (rover_inicio, bateria_inicial, taladro_equipado, carga_actual, tuple(muestras_igneas), tuple(muestras_sedimentarias))
        super(RoverProblem, self).__init__(inicial)
        
        
    def is_goal(self, state):
        posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria = state
        return (len(mIgnea)== 0 and len(mSedimentaria)== 0 and carga == 0)
    
    def actions(self, state):
        posicionRover, bateriaInicial, taladro, carga, mIgnea, mSedimentaria = state
        
        acciones = []
        
        x, y = posicion
        
        movimientos = [
            (x - 1, y),
            (x + 1, y);
            (x, y - 1);
            (x, y + 1);
        ]        
        
        if bateriaInicial > 1:
            for destino in movimientos:
                acciones.append(("moverse", destino))
                
        sobremarchas = [
            (x - 2, y),
            (x + 2, y),
            (x, y - 2),
            (x, y + 2),
        ]
        
        if bateriaInicial > 4:
            for destino in sobremarchas:
                acciones.append(("sobremarcha", destino))
         
        if bateriaInicial > 1:
            if taladro != "termico":
                acciones.append("equipar", "termico")
            
            if taladro != "percusion":
                acciones.append(("equipar", "percusion")) 
                
        if carga > self.capacidad_maxima and bateriaInicial > 3:
            if posicionRover in mIgnea and taladro == "termico":
                acciones.append(("recolectar", "ignea"))
                
            if posicionRover in mSedimentaria and taladro == "percusion":
                acciones.append(("recolectar", "sedimentaria"))
                
        if carga > 0 and bateriaInicial > 1:
            acciones.append(("depositar", None)) 
            
        if posicionRover not in self.zonas_sombra and bateriaInicial < self.bateria_maxima>:
            acciones.append(("recargar", None))
        
        return acciones
    
    
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
        
        if bateriaInicial > 0:
            acciones.append("moverse")
            
        
        return acciones
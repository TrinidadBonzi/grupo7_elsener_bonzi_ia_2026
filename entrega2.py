from simpleai.search import CspProblem, min_conflicts

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    fila, columna = camp_size
    
    variables = []
    dominios = {}
    restricciones = []
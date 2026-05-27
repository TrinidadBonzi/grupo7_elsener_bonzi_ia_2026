from simpleai.search import CspProblem, min_conflicts

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    fila, columna = camp_size
    
    variables = []
    
    for i in range(habs):
        variables.append(("hab", i))
    for i in range(generators):
        variables.append(("gen", i))   
    for i in range(labs):
        variables.append(("lab", i)) 
    for i in range(deposits):
        variables.append(("dep", i))
    for i in range(airlocks):
        variables.append(("air", i))   
    dominios = {}
    restricciones = []
    
    
    
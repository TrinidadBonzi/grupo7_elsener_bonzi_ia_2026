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
        
    posiciones_validas = []

    for f in range(fila):
        for c in range(columna):
            if (f, c) not in craters:
                posiciones_validas.append((f, c))
    
    dominios = {}

    for variable in variables:
        dominios[variable] = posiciones_validas
        
        
    restricciones = []
    
    def noSuperposicion(variables, valores):
        return len(set(valores)) == len(valores)
    
    restricciones.append((variables, noSuperposicion))
    
    def airlockBorde(variables, valores):
        var = variables[0]
        val = valores[0]

        if var[0] != "air":
            return True

        f, c = val

        return (
            f == 0 or
            f == fila - 1 or
            c == 0 or
            c == columna - 1
        )
    for variable in variables:
        if variable[0] == "air":
            restricciones.append(
                ((variable,), airlockBorde)
            )
    
    def habsNoBorde (variables, valores):
        var = variables[0]
        val = valores[0]

        if var[0] != "hab":
            return True

        f, c = val

        return (
            f != 0 and
            f != fila - 1 and
            c != 0 and
            c != columna - 1
        )
    for variable in variables:
        if variable[0] == "hab":
            restricciones.append(
                ((variable,), habsNoBorde)
            )
        
    def SeguridadEnergetica(vars, values):

        (f1, c1), (f2, c2) = values

        return abs(f1 - f2) + abs(c1 - c2) != 1
    for var1 in variables:
        for var2 in variables:

            if var1[0] == "gen" and var2[0] == "hab":

                restricciones.append(
                    ((var1, var2), SeguridadEnergetica)
                )
    def AisalientoGeneradores(vars, values):

        (f1, c1), (f2, c2) = values

        return abs(f1 - f2) + abs(c1 - c2) >= 2
    for var1 in variables:
        for var2 in variables:

            if var1[0] == "gen" and var2[0] == "gen" and var1 != var2:

                restricciones.append(
                    ((var1, var2), AisalientoGeneradores)
                )
    
    
    
    def DepositosCercanos(vars, values):
        (f1, c1), (f2, c2) = values

        return abs(f1 - f2) + abs(c1 - c2) <= 3
    for var1 in variables:
        for var2 in variables:

            if var1[0] == "dep" and var2[0] == "hab":

                restricciones.append(
                    ((var1, var2), DepositosCercanos)
                )
    
   
    
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

    def AislamientoGeneradores(vars, values):

        (f1, c1), (f2, c2) = values

        return abs(f1 - f2) + abs(c1 - c2) >= 2
    for var1 in variables:
        for var2 in variables:

            if var1[0] == "gen" and var2[0] == "gen" and var1 != var2:

                restricciones.append(
                    ((var1, var2), AislamientoGeneradores)
                )
    
    
    def DepositosCercanos(vars, values):
        (f1, c1) = values[0]

        for i in range(len(vars)):
            if vars[i][0] == "dep":
                (f2, c2) = values[i]

                if abs(f1 - f2) + abs(c1 - c2) == 1:
                    return True
        return False
    for var in variables:
        if var[0] == "lab":
            restricciones.append(
                ((var,), DepositosCercanos)
            )
    
    def Evacuacion(vars, values):
            (hr, hc) = values[0]
            
            ocupados = set(values[1:])  # otros módulos

            for dr, dc in [
                (hr-1, hc), (hr+1, hc), (hr, hc-1), (hr, hc+1)
            ]:
                if (dr, dc) not in ocupados and (dr, dc) not in craters:
                    return True
            return False
    for var in variables:
        if var[0] == "hab":
            restricciones.append(
                ((var,), Evacuacion)
            )
    problema = CspProblem(variables, dominios, restricciones)
    solucion = min_conflicts(problema, iterations_limit=1000)
    resultado_final = []
    for var, pos in solucion.items():
        tipo, _id = var
        f, c = pos
        resultado_final.append((tipo, f, c))

    return resultado_final
    
if __name__ == "__main__":
    resultado = build_camp(
    camp_size=(5, 6),
    habs=2,
    generators=1,
    labs=1,
    deposits=2,
    airlocks=1,
    craters=[(2, 2), (2, 3)],
)
    print(resultado)
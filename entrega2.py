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

    if variables == None:
        return []

    for f in range(fila):
        for c in range(columna):
            if (f, c) not in craters:
                posiciones_validas.append((f, c))
    
    dominios = {}

    for variable in variables:
        dominios[variable] = []

        for f, c in posiciones_validas:
            if variable[0] == "air":
                if (
                    f == 0 or
                    f == fila - 1 or
                    c == 0 or
                    c == columna - 1
                ):
                    dominios[variable].append((f, c))
            elif variable[0] == "hab":
                if (
                    f != 0 and
                    f != fila - 1 and
                    c != 0 and
                    c != columna - 1
                ):
                    dominios[variable].append((f, c))
            else:
                dominios[variable].append((f, c))
                     
    restricciones = []
    
    def noSuperposicion(variables, valores): 
        n = len(variables)
        for i in range(n):
            for j in range(n):
                if (i != j):
                   if valores[i] == valores[j]:
                        return False
        return True    
    restricciones.append((variables, noSuperposicion))
        
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

        for i in range(1, len(values)):
            (f2, c2) = values[i]

            if abs(f1 - f2) + abs(c1 - c2) == 1:
                return True
        return False
    for var in variables:
        if var[0] == "lab":
            restriccionv= [var]
            for dep in variables:
                if dep[0] == "dep":
                    restriccionv.append(dep)
            restricciones.append(
                (tuple(restriccionv), DepositosCercanos)
            )
    
    def Evacuacion(vars, values):
            (hr, hc) = values[0]
            
            ocupados = set(values[1:])

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

    for dominio in dominios.values():
        if not dominio:
            return None
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
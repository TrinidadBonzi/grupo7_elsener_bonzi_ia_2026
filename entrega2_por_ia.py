from simpleai.search import CspProblem, min_conflicts

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    rows, cols = camp_size

    # Variables
    variables = []
    for i in range(habs):
        variables.append(f"hab_{i}")
    for i in range(generators):
        variables.append(f"gen_{i}")
    for i in range(labs):
        variables.append(f"lab_{i}")
    for i in range(deposits):
        variables.append(f"dep_{i}")
    for i in range(airlocks):
        variables.append(f"air_{i}")

    # Dominios: todas las celdas menos cráteres
    all_cells = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in craters]
    domains = {var: list(all_cells) for var in variables}

    # Auxiliares
    def es_borde(cell):
        r, c = cell
        return r == 0 or r == rows-1 or c == 0 or c == cols-1

    def adyacentes(cell):
        r, c = cell
        return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

    # Restricciones
    constraints = []

    # 1. Sin superposición
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            def no_superposicion(v1, c1, v2, c2):
                return c1 != c2
            constraints.append(((variables[i], variables[j]), no_superposicion))

    # 3. Esclusas en el borde
    for v in variables:
        if v.startswith("air"):
            def esclusa_borde(var, cell):
                return es_borde(cell)
            constraints.append(((v,), esclusa_borde))

    # 4. Habitacionales al interior
    for v in variables:
        if v.startswith("hab"):
            def hab_interior(var, cell):
                return not es_borde(cell)
            constraints.append(((v,), hab_interior))

    # 5. Generador no junto a hab
    for g in [v for v in variables if v.startswith("gen")]:
        for h in [v for v in variables if v.startswith("hab")]:
            def gen_no_hab(vg, cg, vh, ch):
                return ch not in adyacentes(cg)
            constraints.append(((g, h), gen_no_hab))

    # 6. Generadores aislados
    gens = [v for v in variables if v.startswith("gen")]
    for i in range(len(gens)):
        for j in range(i+1, len(gens)):
            def gen_no_gen(v1, c1, v2, c2):
                return c2 not in adyacentes(c1)
            constraints.append(((gens[i], gens[j]), gen_no_gen))

    # 7. Lab junto a depósito
    labs_vars = [v for v in variables if v.startswith("lab")]
    deps_vars = [v for v in variables if v.startswith("dep")]
    for lab in labs_vars:
        def lab_con_dep(vlab, clab, *dep_pairs):
            dep_cells = dep_pairs[1::2]  # extrae solo los valores
            return any(dep in adyacentes(clab) for dep in dep_cells)
        constraints.append(((lab,) + tuple(deps_vars), lab_con_dep))

    # 8. Hab con ruta libre
    for hab in [v for v in variables if v.startswith("hab")]:
        def hab_ruta(vhab, cell, *others):
            other_cells = others[1::2]  # extrae solo los valores
            ocupadas = set(other_cells) | set(craters)
            return any(
                (0 <= r < rows and 0 <= c < cols) and (r, c) not in ocupadas
                for (r, c) in adyacentes(cell)
            )
        constraints.append(((hab,) + tuple(variables), hab_ruta))

    # Resolver CSP con min_conflicts
    problem = CspProblem(variables, domains, constraints)
    solution = min_conflicts(problem)

    if solution is None:
        return None

    # Convertir a formato pedido
    result = []
    for var, cell in solution.items():
        tipo = var.split("_")[0]
        r, c = cell
        result.append((tipo, r, c))

    return result
from simpleai.search import CspProblem, min_conflicts


def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    rows, cols = camp_size

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

    if not variables:
        return []

    # =========================
    # Funciones auxiliares
    # =========================

    def es_borde(cell):
        r, c = cell
        return (
            r == 0
            or r == rows - 1
            or c == 0
            or c == cols - 1
        )

    def adyacentes(cell):
        r, c = cell

        vecinos = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]

        return [
            (nr, nc)
            for nr, nc in vecinos
            if 0 <= nr < rows and 0 <= nc < cols
        ]

    # =========================
    # Dominios
    # =========================

    all_cells = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if (r, c) not in craters
    ]

    domains = {}

    for var in variables:

        if var.startswith("hab"):
            domains[var] = [
                cell
                for cell in all_cells
                if not es_borde(cell)
            ]

        elif var.startswith("air"):
            domains[var] = [
                cell
                for cell in all_cells
                if es_borde(cell)
            ]

        else:
            domains[var] = list(all_cells)

    # Si algún dominio quedó vacío,
    # el problema es imposible.

    for dominio in domains.values():
        if len(dominio) == 0:
            return None

    # =========================
    # Restricciones
    # =========================

    constraints = []

    # Sin superposición
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):

            def no_superposicion(vars_, values):
                c1, c2 = values
                return c1 != c2

            constraints.append(
                (
                    (variables[i], variables[j]),
                    no_superposicion,
                )
            )

    # Esclusas en borde
    for v in variables:
        if v.startswith("air"):

            def esclusa_borde(vars_, values):
                cell = values[0]
                return es_borde(cell)

            constraints.append(
                (
                    (v,),
                    esclusa_borde,
                )
            )

    # Habitacionales interior
    for v in variables:
        if v.startswith("hab"):

            def hab_interior(vars_, values):
                cell = values[0]
                return not es_borde(cell)

            constraints.append(
                (
                    (v,),
                    hab_interior,
                )
            )

    # Generador no junto a habitacional
    for g in [v for v in variables if v.startswith("gen")]:
        for h in [v for v in variables if v.startswith("hab")]:

            def gen_no_hab(vars_, values):
                cg, ch = values
                return ch not in adyacentes(cg)

            constraints.append(
                (
                    (g, h),
                    gen_no_hab,
                )
            )

    # Generadores aislados
    gens = [v for v in variables if v.startswith("gen")]

    for i in range(len(gens)):
        for j in range(i + 1, len(gens)):

            def gen_no_gen(vars_, values):
                c1, c2 = values
                return c2 not in adyacentes(c1)

            constraints.append(
                (
                    (gens[i], gens[j]),
                    gen_no_gen,
                )
            )

    # Laboratorio junto a algún depósito
    labs_vars = [v for v in variables if v.startswith("lab")]
    deps_vars = [v for v in variables if v.startswith("dep")]

    if labs_vars and not deps_vars:
        return None

    for lab in labs_vars:

        def lab_con_dep(vars_, values):
            clab = values[0]
            dep_cells = values[1:]

            return any(
                dep in adyacentes(clab)
                for dep in dep_cells
            )

        constraints.append(
            (
                (lab,) + tuple(deps_vars),
                lab_con_dep,
            )
        )

    # Ruta de evacuación
    for hab in [v for v in variables if v.startswith("hab")]:

        otras = [v for v in variables if v != hab]

        def hab_ruta(vars_, values):
            cell = values[0]
            other_cells = values[1:]

            ocupadas = set(other_cells) | set(craters)

            return any(
                vecino not in ocupadas
                for vecino in adyacentes(cell)
            )

        constraints.append(
            (
                (hab,) + tuple(otras),
                hab_ruta,
            )
        )

    problem = CspProblem(
        variables,
        domains,
        constraints,
    )

    solution = min_conflicts(problem)

    if solution is None:
        return None

    resultado = []

    for var, (r, c) in solution.items():
        tipo = var.split("_")[0]
        resultado.append((tipo, r, c))

    return resultado
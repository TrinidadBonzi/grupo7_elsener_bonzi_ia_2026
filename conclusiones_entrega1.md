#Conclusiones

Al comparar ambas soluciones vimos que las dos representan información similar dentro de cada estado, como la posición del rover, la batería, el taladro equipado, la carga y las muestras pendientes. Aunque nuestra implementación incorpora algunas restricciones adicionales para que el rover no considere acciones innecesarias y para ajustarse mejor a las condiciones planteadas en la consigna.

Tambien encontramos diferencias en la manera que se generan las acciones posibles. En nuestra implementación intentamos limitar algunas acciones y movimientos como evitar cargar taladros que ya no seran necesarios o cuando conviene hacer depositos. La solución generada por IA, en cambio, permitía más movimientos y acciones posibles en cada estado, haciendo que la búsqueda fuera más grande.

Otra diferencia que encontramos es en la heurística. Nuestra versión tiene en cuenta más aspectos del problema, como los cambios de taladro y las recargas de batería, mientras que la heurística de la IA es más simple. Esto hizo que nuestra búsqueda estuviera mejor guiada hacia la solución.

Si bien ambas soluciones logran modelar el problema, nuestra solución logró superar todos los tests propuestos por la materia, mientras que la generada por IA, presentó fallos en algunos de ellos, especialmente en situaciones ligadas con la acción de depósito. Si bien no logró contemplar las restricciones necesarias, fue útil para comparar enfoques y obtener ideas, pero requirió varias correcciones para adaptarse correctamente al problema. 

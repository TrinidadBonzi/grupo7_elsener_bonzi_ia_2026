#Conclusiones

Ambas soluciones están planteadas de forma diferente. En nuestra implementación intentamos limitar algunas acciones y movimientos para evitar que el rover explore opciones innecesarias. La solución generada por IA, en cambio, permitía más movimientos y acciones posibles en cada estado, haciendo que la búsqueda fuera más grande.

También encontramos diferencias en la heurística. Nuestra versión tiene en cuenta más aspectos del problema, como los cambios de taladro y las recargas de batería, mientras que la heurística de la IA es más simple. Esto hizo que nuestra búsqueda estuviera mejor guiada hacia la solución.

Al probar ambas implementaciones, nuestra solución logró superar todos los tests, mientras que la generada por IA no pudo resolver algunos casos y quedaba trabada en el test 6. 

La solución generada por IA fue útil para comparar enfoques y obtener ideas, pero requirió varias correcciones para adaptarse correctamente al problema. 

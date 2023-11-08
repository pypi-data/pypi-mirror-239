# GTAlib_MonteCarlo - Clase para la Integración Numérica con el Metodo de Monte Carlo

La clase `MonteCarlo` proporciona una forma de realizar la integración numerica de una funcion utilizando el método de Monte Carlo. 

## Requisitos

- Python 3.11.6
- numpy 1.26.1


## Instalación

Para instalar la libreria, utiliza el comando

```bash
pip install GTAlib_MonteCarlo
```


## Uso
La estructura base para implementar la libreria es:

1. Importa la clase `MonteCarlo` en tu script de Python:

    ```python
    from GTAlib_MonteCarlo import MonteCarlo 
    ```
2. Define la funcion que deseas integrar. Puede ser cualquier funcion que acepte un valor `x` y devuelva un valor numerico.

   ```python
   def function(x):
       return x**2  
   ```

3. Crea una instancia de `MonteCarlo` proporcionando los limites de integracion, la funcion y el numero de puntos aleatorios:

   ```python
   a = 0  # Límite inferior de integración
   b = 1  # Límite superior de integración
   n = 100000  # Número de puntos aleatorios
   solver = MonteCarlo(a, b, function, n)
   ```

4. Llama al metodo `MonteCarlo` de la instancia de `MonteCarlo` para calcular la integral:

   ```python
   result = solver.integrate()
   ```

5. El resultado sera un valor numerico que representa la aproximación de la integral de la funcion en el intervalo `[a, b]`.

6. Puedes imprimir el resultado o utilizarlo en tus calculos segun sea necesario.

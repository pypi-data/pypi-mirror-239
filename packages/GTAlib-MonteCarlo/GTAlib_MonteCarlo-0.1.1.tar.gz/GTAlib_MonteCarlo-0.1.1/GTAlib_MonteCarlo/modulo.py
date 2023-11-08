import numpy as np

class MonteCarlo:
    """
    Clase para realizar la integración numérica usando el método de Monte Carlo.

    Args:
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        f (function): Función que se va a integrar.
        n (int): Número de puntos aleatorios para el método de Monte Carlo.

    Attributes:
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        f (function): Función que se va a integrar.
        n (int): Número de puntos aleatorios para el método de Monte Carlo.
    """

    def __init__(self, a, b, f, n):
        self.a = a
        self.b = b
        self.f = f
        self.n = n

    def integrate(self):
        """
        Realiza la integración numérica usando el método de Monte Carlo.

        Returns:
            float: Valor aproximado de la integral de la función en el intervalo [a, b].
        """
        x_values = np.random.uniform(self.a, self.b, self.n)
        y_values = np.random.uniform(0, max(self.f(x_values)), self.n)

        count = np.sum((0 < y_values) & (y_values < self.f(x_values)))

        f_max = max(self.f(x_values))
        A = (self.b - self.a) * f_max

        return (count / self.n) * A
# DataAdjustment

`DataAdjustment` es una clase Python que proporciona funcionalidades para el ajuste de datos utilizando el método del kernel Gaussiano. Esta clase es útil para suavizar series de tiempo de datos, lo que puede ayudar a visualizar tendencias y patrones de manera más clara.

## Requisitos

- Python 3.x
- NumPy
- pandas
- matplotlib


## Uso

```python
# Importar la clase DataAdjustment
from data_adjustment import DataAdjustment

# Crear una instancia de DataAdjustment con el archivo CSV de datos y valor de sigma (opcional)
adjustment = DataAdjustment('datos.csv', sigma=1)

# Graficar la curva suavizada junto con los datos reales
adjustment.plot_smooth_curve()

# Graficar la derivada de la curva suavizada
adjustment.plot_derivative()
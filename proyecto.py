import tkinter as tk
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IndicadoresEconomicos:
    def __init__(self, years):
        self.years = years
        self.data = {
            'Año': list(range(1, years + 1)),
            'PIB': [random.uniform(100, 200) for _ in range(years)],
            'Inflación': [random.uniform(1, 5) for _ in range(years)],
            'Desempleo': [random.uniform(5, 15) for _ in range(years)],
            'Deuda': [random.uniform(30, 70) for _ in range(years)]
        }
        self.df = pd.DataFrame(self.data)

    def simular(self):
        for _ in range(self.years, self.years * 2):
            year = self.df['Año'].iloc[-1] + 1
            pib = random.uniform(self.df['PIB'].iloc[-1] - 10, self.df['PIB'].iloc[-1] + 10)
            inflacion = random.uniform(1, 5)
            desempleo = random.uniform(5, 15)
            deuda = random.uniform(30, 70)
            self.df = self.df.append({'Año': year, 'PIB': pib, 'Inflación': inflacion, 'Desempleo': desempleo, 'Deuda': deuda}, ignore_index=True)

class MercadoAcciones:
    def __init__(self, symbols, years):
        self.symbols = symbols
        self.years = years
        self.data = {
            'Año': list(range(1, years + 1))
        }
        for symbol in symbols:
            self.data[symbol] = [random.uniform(100, 2000) for _ in range(years)]
        self.df = pd.DataFrame(self.data)

    def obtener_precio_accion(self, symbol, year):
        return self.df[symbol].iloc[year - 1]

class Usuario:
    def __init__(self, nombre, dinero_inicial):
        self.nombre = nombre
        self.dinero_disponible = dinero_inicial
        self.inversiones = {}
        self.transacciones = []

    def invertir(self, mercado, symbol, cantidad, year):
        precio_accion = mercado.obtener_precio_accion(symbol, year)
        costo_total = precio_accion * cantidad
        if costo_total <= self.dinero_disponible:
            if symbol in self.inversiones:
                self.inversiones[symbol] += cantidad
            else:
                self.inversiones[symbol] = cantidad
            self.dinero_disponible -= costo_total
            self.transacciones.append(f"Inversión: Compra de {cantidad} acciones de {symbol} por {precio_accion} cada una en el año {year}.")
            return True
        else:
            return False

    def vender_inversion(self, mercado, symbol, cantidad, year):
        if symbol in self.inversiones and cantidad <= self.inversiones[symbol]:
            precio_accion = mercado.obtener_precio_accion(symbol, year)
            ingresos = precio_accion * cantidad
            self.inversiones[symbol] -= cantidad
            self.dinero_disponible += ingresos
            self.transacciones.append(f"Inversión: Venta de {cantidad} acciones de {symbol} por {precio_accion} cada una en el año {year}.")
            return ingresos
        else:
            return 0

# Funciones para manejar las acciones del usuario
def invertir_accion():
    symbol = symbol_entry.get()
    cantidad = int(cantidad_entry.get())
    year = int(year_entry.get())
    if usuario.invertir(mercado, symbol, cantidad, year):
        resultado_label.config(text=f"Inversión exitosa en {cantidad} acciones de {symbol} en el año {year}.")
    else:
        resultado_label.config(text=f"No hay suficiente dinero para invertir en {symbol} en el año {year}.")

def vender_accion():
    symbol = symbol_entry.get()
    cantidad = int(cantidad_entry.get())
    year = int(year_entry.get())
    ingresos = usuario.vender_inversion(mercado, symbol, cantidad, year)
    resultado_label.config(text=f"Ingresos por venta de {cantidad} acciones de {symbol}: {ingresos}.")

def mostrar_grafica():
    fig = plt.figure(figsize=(8, 6))
    for symbol in symbols:
        plt.plot(mercado.df['Año'], mercado.df[symbol], marker='o', label=symbol)
    plt.xlabel('Año')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=7, column=0, columnspan=2)

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Simulador Económico y Financiero")

# Crear y posicionar los elementos en la interfaz
tk.Label(ventana, text="Symbol:").grid(row=0, column=0)
tk.Label(ventana, text="Cantidad:").grid(row=1, column=0)
tk.Label(ventana, text="Año:").grid(row=2, column=0)

symbol_entry = tk.Entry(ventana)
cantidad_entry = tk.Entry(ventana)
year_entry = tk.Entry(ventana)

symbol_entry.grid(row=0, column=1)
cantidad_entry.grid(row=1, column=1)
year_entry.grid(row=2, column=1)

invertir_button = tk.Button(ventana, text="Invertir", command=invertir_accion)
vender_button = tk.Button(ventana, text="Vender", command=vender_accion)
grafica_button = tk.Button(ventana, text="Mostrar Gráfica", command=mostrar_grafica)
resultado_label = tk.Label(ventana, text="Resultados")

invertir_button.grid(row=3, column=0)
vender_button.grid(row=3, column=1)
grafica_button.grid(row=4, column=0, columnspan=2)
resultado_label.grid(row=5, column=0, columnspan=2)

# Inicializar objetos de las clases
years = 10
symbols = ['AAPL', 'GOOG', 'AMZN']
indicadores = IndicadoresEconomicos(years)
mercado = MercadoAcciones(symbols, years)
usuario = Usuario("Usuario", dinero_inicial=100000)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()

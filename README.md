# Parallel Sum of Squares in Python

This project demonstrates the performance difference between **sequential** and **parallel** processing in Python using the `multiprocessing` module. The program calculates the **sum of squares** of a large list of integers both sequentially and using multiple processes.

## Features

- Sequential computation of sum of squares
- Parallel computation using Python's `multiprocessing`
- Automatic CPU core detection
- Runtime comparison and verification of results
- Demonstrates real-world performance trade-offs

## 🛠Requirements

- Python 3.6+
- Cross-platform (Windows, macOS, Linux)

## How It Works

1. Generates a list of integers from 1 to 20,000,000.
2. Computes the sum of squares:
   - **Sequentially** in a single loop.
   - **In parallel**, by:
     - Splitting the list into chunks
     - Launching one process per CPU core
     - Summing squares in each process
     - Collecting and aggregating results via a queue
3. Compares execution times and results.

## Usage

Run the script:

```bash
python sum_squares_parallel.py
```

## Output
```bash
Lista generada con 20000000 elementos.

--- Iniciando Cálculo Secuencial ---
Suma total (secuencial): 266666673333333000000
Tiempo (secuencial): 6.84 segundos

--- Iniciando Cálculo Paralelo ---
Utilizando 8 procesos (núcleos disponibles).
...
Suma total (paralela): 266666673333333000000
Tiempo (paralelo): 2.17 segundos

¡Los resultados de la suma coinciden!
El cálculo paralelo fue 3.15 veces más rápido.
```

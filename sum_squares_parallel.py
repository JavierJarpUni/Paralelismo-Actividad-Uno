import multiprocessing
import time
import os

# Función que cada proceso ejecutará para calcular la suma de cuadrados de una porción de la lista
def sum_squares_worker(numbers, result_queue):
    """Calcula la suma de cuadrados para una lista de números y la pone en la cola."""
    print(f"Proceso {os.getpid()} iniciando con {len(numbers)} elementos.")
    local_sum = 0
    for n in numbers:
        local_sum += n * n
    result_queue.put(local_sum)
    print(f"Proceso {os.getpid()} finalizado.")

if __name__ == "__main__":
    # Generar una lista grande de números
    # (Para una demostración más rápida, puedes reducir este número, ej. 1_000_000)
    large_list = list(range(1, 20_000_001)) 
    list_size = len(large_list)
    print(f"Lista generada con {list_size} elementos.")

    # --- Versión Secuencial (para comparación) ---
    print("\n--- Iniciando Cálculo Secuencial ---")
    start_time_sequential = time.time()
    total_sum_sequential = 0
    for n in large_list:
        total_sum_sequential += n * n
    end_time_sequential = time.time()
    time_sequential = end_time_sequential - start_time_sequential
    print(f"Suma total (secuencial): {total_sum_sequential}")
    print(f"Tiempo (secuencial): {time_sequential:.4f} segundos")

    # --- Versión Paralela ---
    print("\n--- Iniciando Cálculo Paralelo ---")
    start_time_parallel = time.time()

    # Determinar el número de procesos a utilizar (generalmente igual al número de núcleos de CPU)
    num_processes = multiprocessing.cpu_count()
    print(f"Utilizando {num_processes} procesos (núcleos disponibles).")

    # Dividir la lista en trozos (chunks) para cada proceso
    chunk_size = list_size // num_processes
    chunks = []
    for i in range(num_processes):
        start_index = i * chunk_size
        # El último proceso toma todos los elementos restantes
        if i == num_processes - 1:
            end_index = list_size
        else:
            end_index = (i + 1) * chunk_size
        chunks.append(large_list[start_index:end_index])

    # Cola para recolectar los resultados de cada proceso
    result_queue = multiprocessing.Queue()
    processes = []

    # Crear e iniciar los procesos
    for i in range(num_processes):
        # Asegurarse de que haya un chunk para el proceso (si list_size < num_processes)
        if i < len(chunks) and len(chunks[i]) > 0:
            process = multiprocessing.Process(target=sum_squares_worker, args=(chunks[i], result_queue))
            processes.append(process)
            process.start()
        elif i >= len(chunks): # No hay más chunks para más procesos
            print(f"Advertencia: Menos chunks ({len(chunks)}) que procesos ({num_processes}). Proceso {i} no iniciado.")


    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    # Recolectar resultados de la cola
    total_sum_parallel = 0
    while not result_queue.empty():
        total_sum_parallel += result_queue.get()
    
    end_time_parallel = time.time()
    time_parallel = end_time_parallel - start_time_parallel
    print(f"Suma total (paralela): {total_sum_parallel}")
    print(f"Tiempo (paralelo): {time_parallel:.4f} segundos")

    # Verificación y comparación
    if total_sum_parallel == total_sum_sequential:
        print("\n¡Los resultados de la suma coinciden!")
    else:
        print("\n¡ERROR! Los resultados de la suma NO coinciden.")
        print(f"Secuencial: {total_sum_sequential}, Paralelo: {total_sum_parallel}")

    if time_parallel < time_sequential and num_processes > 1 and processes: # Asegurar que hubo paralelismo
        speedup = time_sequential / time_parallel
        print(f"El cálculo paralelo fue {speedup:.2f} veces más rápido.")
    elif not processes:
        print("No se ejecutaron procesos en paralelo (lista muy pequeña o problema con chunks).")
    else:
        print("El cálculo paralelo no fue más rápido (puede ocurrir con listas pequeñas o sobrecarga de procesos).")
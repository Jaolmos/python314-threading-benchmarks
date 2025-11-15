"""
Test de rendimiento: Calculo intensivo de suma de cuadrados
Compara ejecucion secuencial vs paralela con threads
"""
import threading
import time
import sys


def calculate_squares(start, end, results, index):
    """Calcula la suma de cuadrados en un rango"""
    total = 0
    for i in range(start, end):
        total += i * i
    results[index] = total


def run_sequential(ranges):
    """Ejecuta las tareas de forma secuencial"""
    results = [0] * len(ranges)
    start = time.time()
    
    for i, (start_range, end_range) in enumerate(ranges):
        calculate_squares(start_range, end_range, results, i)
    
    elapsed = time.time() - start
    return elapsed, sum(results)


def run_parallel(ranges):
    """Ejecuta las tareas en paralelo usando threads"""
    results = [0] * len(ranges)
    threads = []
    start = time.time()
    
    # Crear y lanzar threads
    for i, (start_range, end_range) in enumerate(ranges):
        t = threading.Thread(target=calculate_squares, args=(start_range, end_range, results, i))
        threads.append(t)
        t.start()
    
    # Esperar a que todos los threads completen su ejecucion
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    return elapsed, sum(results)


if __name__ == "__main__":
    print("=" * 60)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("=" * 60)
    
    # Dividir el rango en partes iguales
    TOTAL = 10_000_000
    NUM_THREADS = 4
    RANGE_SIZE = TOTAL // NUM_THREADS
    
    ranges = []
    for i in range(NUM_THREADS):
        start = i * RANGE_SIZE
        end = start + RANGE_SIZE
        ranges.append((start, end))
    
    print(f"\nPrueba: Suma de cuadrados hasta {TOTAL:,} en {NUM_THREADS} rangos")
    print("-" * 60)
    
    # Prueba secuencial
    print("\n[1] Ejecucion secuencial")
    time_seq, result_seq = run_sequential(ranges)
    print(f"Tiempo: {time_seq:.3f} segundos")
    
    # Prueba paralela
    print("\n[2] Ejecucion paralela (threads)")
    time_par, result_par = run_parallel(ranges)
    print(f"Tiempo: {time_par:.3f} segundos")
    
    # Analisis
    print("\n" + "=" * 60)
    if time_par < time_seq:
        speedup = time_seq / time_par
        print(f"Resultado: Speedup de {speedup:.2f}x (mas rapido)")
    else:
        slowdown = time_par / time_seq
        print(f"Resultado: Slowdown de {slowdown:.2f}x (mas lento, efecto GIL)")
    print("=" * 60)


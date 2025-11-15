"""
Test de rendimiento: Calculo intensivo de suma de cuadrados
Compara ejecucion secuencial vs paralela con threads
"""
import threading
import time
import sys


def calculate_squares(n, results, index):
    """Calcula la suma de cuadrados hasta n"""
    total = 0
    for i in range(n):
        total += i * i
    results[index] = total


def run_sequential(num_tasks, n):
    """Ejecuta las tareas de forma secuencial"""
    results = [0] * num_tasks
    start = time.time()
    
    for i in range(num_tasks):
        calculate_squares(n, results, i)
    
    elapsed = time.time() - start
    return elapsed, sum(results)


def run_parallel(num_threads, n):
    """Ejecuta las tareas en paralelo usando threads"""
    results = [0] * num_threads
    threads = []
    start = time.time()
    
    # Crear y lanzar threads
    for i in range(num_threads):
        t = threading.Thread(target=calculate_squares, args=(n, results, i))
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
    
    NUM_THREADS = 4
    N = 10_000_000
    
    print(f"\nPrueba: {NUM_THREADS} tareas, {N:,} iteraciones cada una")
    print("-" * 60)
    
    # Prueba secuencial
    print("\n[1] Ejecucion secuencial")
    time_seq, result_seq = run_sequential(NUM_THREADS, N)
    print(f"Tiempo: {time_seq:.3f} segundos")
    
    # Prueba paralela
    print("\n[2] Ejecucion paralela (threads)")
    time_par, result_par = run_parallel(NUM_THREADS, N)
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


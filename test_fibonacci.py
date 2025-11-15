"""
Test de rendimiento: Calculo de Fibonacci
Compara ejecucion secuencial vs paralela con threads
"""
import threading
import time
import sys


def fibonacci(n, results, index):
    """Calcula el n-esimo numero de Fibonacci"""
    if n <= 1:
        results[index] = n
        return
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    results[index] = b


def run_sequential(fibonacci_numbers):
    """Ejecuta las tareas de forma secuencial"""
    results = [0] * len(fibonacci_numbers)
    start = time.time()
    
    for i, n in enumerate(fibonacci_numbers):
        fibonacci(n, results, i)
    
    elapsed = time.time() - start
    return elapsed, results


def run_parallel(fibonacci_numbers):
    """Ejecuta las tareas en paralelo usando threads"""
    results = [0] * len(fibonacci_numbers)
    threads = []
    start = time.time()
    
    # Crear y lanzar threads
    for i, n in enumerate(fibonacci_numbers):
        t = threading.Thread(target=fibonacci, args=(n, results, i))
        threads.append(t)
        t.start()
    
    # Esperar a que todos los threads completen su ejecucion
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    return elapsed, results


if __name__ == "__main__":
    print("=" * 60)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("=" * 60)
    
    # Cada thread calcula un Fibonacci diferente (numeros balanceados)
    NUM_THREADS = 4
    fibonacci_numbers = [350_000, 375_000, 400_000, 425_000]
    
    print(f"\nPrueba: {NUM_THREADS} calculos de Fibonacci diferentes")
    print(f"Numeros: {', '.join([f'{n:,}' for n in fibonacci_numbers])}")
    print("-" * 60)
    
    # Prueba secuencial
    print("\n[1] Ejecucion secuencial")
    time_seq, result_seq = run_sequential(fibonacci_numbers)
    print(f"Tiempo: {time_seq:.3f} segundos")
    
    # Prueba paralela
    print("\n[2] Ejecucion paralela (threads)")
    time_par, result_par = run_parallel(fibonacci_numbers)
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


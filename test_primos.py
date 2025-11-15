"""
Test de rendimiento: Busqueda de numeros primos
Compara ejecucion secuencial vs paralela con threads
"""
import threading
import time
import sys


def is_prime(n):
    """Verifica si un numero es primo"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def count_primes(start, end, results, index):
    """Cuenta cuantos primos hay en un rango"""
    count = 0
    for n in range(start, end):
        if is_prime(n):
            count += 1
    results[index] = count


def run_sequential(ranges):
    """Ejecuta el conteo de forma secuencial"""
    results = [0] * len(ranges)
    start = time.time()
    
    for i, (start_range, end_range) in enumerate(ranges):
        count_primes(start_range, end_range, results, i)
    
    elapsed = time.time() - start
    return elapsed, sum(results)


def run_parallel(ranges):
    """Ejecuta el conteo en paralelo usando threads"""
    results = [0] * len(ranges)
    threads = []
    start = time.time()
    
    # Crear y lanzar threads
    for i, (start_range, end_range) in enumerate(ranges):
        t = threading.Thread(target=count_primes, args=(start_range, end_range, results, i))
        threads.append(t)
        t.start()
    
    # Esperar a que terminen
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    return elapsed, sum(results)


if __name__ == "__main__":
    print("=" * 60)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("=" * 60)
    
    # Dividir el rango en 4 partes
    TOTAL = 500_000
    NUM_PARTS = 4
    RANGE_SIZE = TOTAL // NUM_PARTS
    
    ranges = []
    for i in range(NUM_PARTS):
        start = i * RANGE_SIZE
        end = start + RANGE_SIZE
        ranges.append((start, end))
    
    print(f"\nBuscando primos hasta {TOTAL:,} en {NUM_PARTS} rangos")
    print("-" * 60)
    
    # Prueba secuencial
    print("\n[1] Ejecucion secuencial")
    time_seq, primes_seq = run_sequential(ranges)
    print(f"Tiempo: {time_seq:.3f} segundos")
    print(f"Primos encontrados: {primes_seq:,}")
    
    # Prueba paralela
    print("\n[2] Ejecucion paralela (threads)")
    time_par, primes_par = run_parallel(ranges)
    print(f"Tiempo: {time_par:.3f} segundos")
    print(f"Primos encontrados: {primes_par:,}")
    
    # Analisis
    print("\n" + "=" * 60)
    if time_par < time_seq:
        speedup = time_seq / time_par
        print(f"Resultado: Speedup de {speedup:.2f}x (mas rapido)")
    else:
        slowdown = time_par / time_seq
        print(f"Resultado: Slowdown de {slowdown:.2f}x (mas lento, efecto GIL)")
    print("=" * 60)


# Benchmark: Python 3.12 vs 3.14 (GIL vs sin GIL)

Proyecto de comparación de rendimiento entre diferentes versiones de Python con y sin GIL (Global Interpreter Lock).

## ¿Qué es el GIL?

El **GIL (Global Interpreter Lock)** es un mecanismo que permite que solo un thread ejecute código Python a la vez. Esto limita el rendimiento cuando usamos multithreading en tareas intensivas de CPU.

Python 3.14 introduce oficialmente soporte para **free-threaded Python** (sin GIL), permitiendo verdadero paralelismo en threads.

## Versiones comparadas

- **Python 3.12.3** - Versión estable con GIL
- **Python 3.14.0** - Última versión con GIL
- **Python 3.14.0+freethreaded** - Última versión sin GIL

## Instalación

### 1. Instalar uv

`uv` es un gestor ultrarapido de entornos Python (escrito en Rust).

**Opción 1 (recomendada):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Opción 2 (con pip):**
```bash
pip install uv
```

**Alternativas:** `pyenv` o `conda`.

### 2. Instalar versiones de Python

```bash
# Python 3.14.0 con GIL
uv python install 3.14

# Python 3.14.0 sin GIL (free-threaded)
uv python install 3.14t
```

### 3. Verificar instalación

```bash
uv python list
```

## Archivos del proyecto

- `test_suma_cuadrados.py` - Test de cálculo intensivo de suma de cuadrados
- `test_primos.py` - Test con búsqueda de números primos
- `test_fibonacci.py` - Test con cálculo de números de Fibonacci
- `test_version.py` - Script simple para verificar versión de Python
- `run_benchmarks.sh` - Script para ejecutar todos los benchmarks automáticamente
- `demo_versiones.sh` - Script para demostrar cómo cambiar entre versiones
- `pyproject.toml` - Configuración del proyecto para uv

## Ejecutar las pruebas

### Opción 1: Ejecutar todos los benchmarks automáticamente

```bash
./run_benchmarks.sh
```

Esto ejecutará todos los tests con las 3 versiones de Python y guardará automáticamente los resultados en un archivo `resultados_YYYYMMDD_HHMMSS.txt`.

### Opción 2: Ejecutar tests individuales

**Test de suma de cuadrados:**

```bash
uv run --python 3.12.3 test_suma_cuadrados.py
uv run --python 3.14 test_suma_cuadrados.py
uv run --python 3.14t test_suma_cuadrados.py
```

**Test de Fibonacci:**

```bash
uv run --python 3.12.3 test_fibonacci.py
uv run --python 3.14t test_fibonacci.py
```

**Test de números primos:**

```bash
uv run --python 3.12.3 test_primos.py
uv run --python 3.14t test_primos.py
```

## Entorno de pruebas

Las pruebas se realizaron en:
- **Procesador:** AMD Ryzen 7 (16 cores)
- **Sistema Operativo:** Ubuntu 24.04.3 LTS
- **Kernel:** Linux 6.14.0-33-generic
- **Threads utilizados:** 4 (de 16 núcleos disponibles)

## Resultados obtenidos

Todos los benchmarks se ejecutan con **4 threads** para aprovechar múltiples núcleos de CPU.

### Test 1: Suma de cuadrados

Cálculo de suma de cuadrados hasta 10 millones, dividido en 4 rangos.

| Versión | Secuencial | Paralelo | Resultado |
|---------|-----------|----------|-----------|
| Python 3.12.3 (GIL) | 0.545s | 0.602s | Slowdown 1.10x |
| Python 3.14.0 (GIL) | 0.387s | 0.457s | Slowdown 1.18x |
| Python 3.14.0t (sin GIL) | 0.390s | 0.109s | **Speedup 3.58x** |

### Test 2: Búsqueda de números primos

Busca números primos hasta 500,000 en 4 rangos. Encuentra 41,538 números primos.

| Versión | Secuencial | Paralelo | Resultado |
|---------|-----------|----------|-----------|
| Python 3.12.3 (GIL) | 0.443s | 0.543s | Slowdown 1.22x |
| Python 3.14.0 (GIL) | 0.377s | 0.458s | Slowdown 1.21x |
| Python 3.14.0t (sin GIL) | 0.434s | 0.156s | **Speedup 2.79x** |

### Test 3: Fibonacci

Calcula 4 números de Fibonacci diferentes: Fib(350K), Fib(375K), Fib(400K), Fib(425K).

| Versión | Secuencial | Paralelo | Resultado |
|---------|-----------|----------|-----------|
| Python 3.12.3 (GIL) | 4.385s | 5.178s | Slowdown 1.18x |
| Python 3.14.0 (GIL) | 5.801s | 7.257s | Slowdown 1.25x |
| Python 3.14.0t (sin GIL) | 5.791s | 1.801s | **Speedup 3.22x** |

## Interpretar los resultados

### Slowdown (más lento)

Cuando el resultado muestra "Slowdown", significa que usar multithreading fue **más lento** que ejecutar todo secuencialmente. Esto ocurre por el GIL:

- El GIL impide que los threads se ejecuten realmente en paralelo
- Los threads se turnan para ejecutarse
- Hay overhead (costo adicional) por gestionar los threads
- Resultado: Peor rendimiento que hacer todo de forma secuencial

### Speedup (más rápido)

Cuando el resultado muestra "Speedup", significa que usar multithreading fue **más rápido** que ejecutar todo secuencialmente. Esto ocurre sin el GIL:

- Los threads pueden ejecutarse simultáneamente en diferentes núcleos de CPU
- Aprovecha el paralelismo real del hardware
- Speedup de 3.59x significa que es casi 4 veces más rápido
- Resultado: Mucho mejor rendimiento

## Conclusiones

### Paralelismo real con Python 3.14t sin GIL

Los resultados demuestran que **Python 3.14t sin GIL logra paralelismo real** usando los 4 threads:

1. **Con GIL (Python 3.12/3.14)**: El multithreading es **10-25% más lento** que secuencial
   - Los 4 threads se turnan (solo 1 ejecuta a la vez)
   - Hay overhead por gestionar threads sin beneficio
   - **No hay paralelismo real**

2. **Sin GIL (Python 3.14t)**: El multithreading es **~3x más rápido** que secuencial
   - Los 4 threads ejecutan simultáneamente en 4 núcleos de CPU
   - Aprovecha el paralelismo real del hardware
   - **Paralelismo real** ✅

3. **Speedup promedio con 4 threads**: **3.20x** (cercano al ideal de 4x)
   - Suma de cuadrados: 3.58x
   - Búsqueda de primos: 2.79x
   - Fibonacci: 3.22x

4. **Python 3.14t es el futuro** para aplicaciones con procesamiento paralelo intensivo

## ¿Cuándo usar cada versión?

**Python 3.12/3.14 con GIL:**
- Aplicaciones que no usan multithreading intensivo
- Scripts simples
- Compatibilidad con librerías existentes

**Python 3.14 sin GIL:**
- Aplicaciones con procesamiento paralelo intensivo
- Servidores web con muchas conexiones simultáneas
- Análisis de datos con múltiples threads
- Cualquier código CPU-intensivo que use threads

## Recursos adicionales

- [Python 3.14.0 Release Notes](https://www.python.org/downloads/release/python-3140/)
- [PEP 779: Free-threaded Python](https://peps.python.org/pep-0779/)
- [Documentación de uv](https://github.com/astral-sh/uv)
- [Documentación de threading](https://docs.python.org/3/library/threading.html)

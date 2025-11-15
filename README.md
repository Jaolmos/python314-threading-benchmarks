# Benchmark: Python 3.12 vs 3.14 (GIL vs No-GIL)

Proyecto de comparacion de rendimiento entre diferentes versiones de Python con y sin GIL (Global Interpreter Lock).

## Que es el GIL

El **GIL (Global Interpreter Lock)** es un mecanismo que permite que solo un thread ejecute codigo Python a la vez. Esto limita el rendimiento cuando usamos multithreading en tareas intensivas de CPU.

Python 3.14 introduce oficialmente soporte para **free-threaded Python** (sin GIL), permitiendo verdadero paralelismo en threads.

## Versiones comparadas

- **Python 3.12.3** - Version estable con GIL (tu version actual del sistema)
- **Python 3.14.0** - Version nueva con GIL (para ver mejoras generales)
- **Python 3.14.0+freethreaded** - Version nueva SIN GIL (la estrella del show)

## Instalacion

### 1. Instalar uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Instalar versiones de Python

```bash
# Python 3.14.0 con GIL
uv python install cpython-3.14.0-linux-x86_64-gnu

# Python 3.14.0 sin GIL (free-threaded)
uv python install cpython-3.14.0+freethreaded-linux-x86_64-gnu
```

### 3. Verificar instalacion

```bash
uv python list
```

## Archivos del proyecto

- `test_calculos.py` - Test con calculos matematicos intensivos (suma de cuadrados)
- `test_primos.py` - Test con busqueda de numeros primos
- `test_fibonacci.py` - Test con calculo de numeros de Fibonacci
- `test_version.py` - Script simple para verificar version de Python
- `run_benchmarks.sh` - Script para ejecutar todos los benchmarks automaticamente
- `demo_versiones.sh` - Script para demostrar como cambiar entre versiones
- `PROGRESO.md` - Memoria del proyecto con estado actual y resultados
- `pyproject.toml` - Configuracion del proyecto para uv

## Ejecutar las pruebas

### Opcion 1: Ejecutar todos los benchmarks automaticamente

```bash
./run_benchmarks.sh
```

Esto ejecutara todos los tests con las 3 versiones de Python y guardara automaticamente los resultados en un archivo `resultados_YYYYMMDD_HHMMSS.txt`.

### Opcion 2: Ejecutar tests individuales

**Test de calculos matematicos:**

```bash
uv run --python 3.12.3 test_calculos.py
uv run --python cpython-3.14.0-linux-x86_64-gnu test_calculos.py
uv run --python cpython-3.14.0+freethreaded-linux-x86_64-gnu test_calculos.py
```

**Test de Fibonacci:**

```bash
uv run --python 3.12.3 test_fibonacci.py
uv run --python cpython-3.14.0+freethreaded-linux-x86_64-gnu test_fibonacci.py
```

**Test de numeros primos:**

```bash
uv run --python 3.12.3 test_primos.py
uv run --python cpython-3.14.0+freethreaded-linux-x86_64-gnu test_primos.py
```

## Resultados obtenidos

### Test 1: Calculos matematicos (suma de cuadrados)

| Version | Secuencial | Paralelo | Resultado |
|---------|-----------|----------|-----------|
| Python 3.12.3 (GIL) | 2.182s | 2.467s | Slowdown 1.13x |
| Python 3.14.0 (GIL) | 1.683s | 1.909s | Slowdown 1.13x |
| Python 3.14.0t (sin GIL) | 1.541s | 0.429s | **Speedup 3.59x** |

### Test 2: Busqueda de numeros primos

| Version | Secuencial | Paralelo | Resultado |
|---------|-----------|----------|-----------|
| Python 3.12.3 (GIL) | 0.438s | 0.537s | Slowdown 1.23x |
| Python 3.14.0 (GIL) | 0.378s | 0.462s | Slowdown 1.22x |
| Python 3.14.0t (sin GIL) | 0.437s | 0.163s | **Speedup 2.69x** |

## Interpretar los resultados

### Slowdown (mas lento)

Cuando el resultado muestra "Slowdown", significa que usar multithreading fue **mas lento** que ejecutar todo secuencialmente. Esto ocurre por el GIL:

- El GIL impide que los threads se ejecuten realmente en paralelo
- Los threads se turnan para ejecutarse
- Hay overhead (costo adicional) por gestionar los threads
- Resultado: Peor rendimiento que hacer todo de forma secuencial

### Speedup (mas rapido)

Cuando el resultado muestra "Speedup", significa que usar multithreading fue **mas rapido** que ejecutar todo secuencialmente. Esto ocurre sin el GIL:

- Los threads pueden ejecutarse simultaneamente en diferentes nucleos de CPU
- Aprovecha el paralelismo real del hardware
- Speedup de 3.59x significa que es casi 4 veces mas rapido
- Resultado: Mucho mejor rendimiento

## Conclusiones

1. **El GIL si limita el rendimiento**: Python 3.12 y 3.14 con GIL son 13-23% mas lentos con multithreading
2. **Python 3.14 sin GIL es impresionante**: 2.5-3.5x mas rapido en tareas paralelas
3. **Python 3.14 es mas rapido en general**: Incluso con GIL, tiene mejoras de optimizacion
4. **Multithreading vale la pena sin GIL**: Si tu codigo usa threads, Python 3.14t es el futuro

## Cuando usar cada version

**Python 3.12/3.14 con GIL:**
- Aplicaciones que no usan multithreading intensivo
- Scripts simples
- Compatibilidad con librerias existentes

**Python 3.14 sin GIL:**
- Aplicaciones con procesamiento paralelo intensivo
- Servidores web con muchas conexiones simultaneas
- Analisis de datos con multiples threads
- Cualquier codigo CPU-intensivo que use threads

## Recursos adicionales

- [Python 3.14.0 Release Notes](https://www.python.org/downloads/release/python-3140/)
- [PEP 779: Free-threaded Python](https://peps.python.org/pep-0779/)
- [Documentacion de uv](https://github.com/astral-sh/uv)
- [Documentacion de threading](https://docs.python.org/3/library/threading.html)

## Notas tecnicas

- uv gestiona entornos virtuales automaticamente, no necesitas activarlos manualmente
- Cada version de Python tiene su propio entorno aislado
- Los benchmarks usan 4 threads para aprovechar multiples nucleos
- El archivo `.venv` se recrea automaticamente al cambiar de version

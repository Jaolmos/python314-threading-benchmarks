# Benchmark: Python 3.12 vs 3.14 (GIL vs No-GIL)

## Estado actual
- [x] Instalar uv
- [x] Instalar Python 3.14.0 (con GIL)
- [x] Instalar Python 3.14.0+freethreaded (sin GIL)
- [x] Crear pyproject.toml
- [x] Crear scripts de prueba
- [x] Ejecutar benchmarks
- [x] Analizar resultados
- [x] Crear test adicional (Fibonacci)

## Versiones instaladas
- **Python 3.12.3**: /usr/bin/python3.12 (sistema)
- **Python 3.14.0**: /home/jose/.local/bin/python3.14 (con GIL)
- **Python 3.14.0t**: /home/jose/.local/bin/python3.14t (sin GIL - freethreaded)

## Objetivo
Comparar el rendimiento de multithreading en tareas intensivas de CPU:
- Con GIL: Los threads no pueden ejecutarse realmente en paralelo
- Sin GIL: Los threads pueden usar múltiples núcleos simultáneamente

## Pruebas realizadas
1. Cálculo matemático intensivo (suma de cuadrados)
2. Búsqueda de números primos
3. Cálculo de Fibonacci (nuevo)

## Resultados principales

### Test 1: Cálculos matemáticos
- Python 3.12.3 (GIL): Slowdown 1.13x
- Python 3.14.0 (GIL): Slowdown 1.13x
- Python 3.14.0t (sin GIL): **Speedup 3.59x** ⚡

### Test 2: Búsqueda de primos
- Python 3.12.3 (GIL): Slowdown 1.23x
- Python 3.14.0 (GIL): Slowdown 1.22x
- Python 3.14.0t (sin GIL): **Speedup 2.69x** ⚡

### Conclusión
Python 3.14.0+freethreaded (sin GIL) es 2-3.5x más rápido en multithreading.

## Notas
- uv gestiona las versiones automáticamente, no necesitamos crear entornos manualmente
- Usaremos `uv run --python VERSION script.py` para ejecutar con cada versión


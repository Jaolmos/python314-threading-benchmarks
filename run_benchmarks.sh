#!/bin/bash
# Script para ejecutar benchmarks con 3 versiones de Python

cd /home/jose/Escritorio/practica-programacion/python/rendimiento-python314

# Crear nombre de archivo con fecha y hora
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_FILE="resultados_${TIMESTAMP}.txt"

# Funcion para ejecutar un test
run_test() {
    local version=$1
    local label=$2
    local script=$3
    
    echo ""
    echo "----------------------------------------"
    echo "Test: $label"
    echo "----------------------------------------"
    uv run --python "$version" "$script"
    sleep 1
}

# Funcion principal que ejecuta todo
main() {
    echo ""
    echo "========================================================"
    echo "  Benchmark: Python 3.12 vs 3.14 (GIL vs sin GIL)"
    echo "========================================================"
    echo "  Guardando resultados en: $RESULTS_FILE"
    echo "========================================================"
    echo ""

    # Test 1: Calculos matematicos
    echo ""
    echo "######## TEST 1: CALCULOS MATEMATICOS ########"

    run_test "3.12.3" "Python 3.12.3 (con GIL)" "test_calculos.py"
    run_test "3.14" "Python 3.14.0 (con GIL)" "test_calculos.py"
    run_test "3.14t" "Python 3.14.0t (sin GIL)" "test_calculos.py"

    # Test 2: Numeros primos
    echo ""
    echo ""
    echo "######## TEST 2: BUSQUEDA DE PRIMOS ########"

    run_test "3.12.3" "Python 3.12.3 (con GIL)" "test_primos.py"
    run_test "3.14" "Python 3.14.0 (con GIL)" "test_primos.py"
    run_test "3.14t" "Python 3.14.0t (sin GIL)" "test_primos.py"

    # Test 3: Fibonacci
    echo ""
    echo ""
    echo "######## TEST 3: FIBONACCI ########"

    run_test "3.12.3" "Python 3.12.3 (con GIL)" "test_fibonacci.py"
    run_test "3.14" "Python 3.14.0 (con GIL)" "test_fibonacci.py"
    run_test "3.14t" "Python 3.14.0t (sin GIL)" "test_fibonacci.py"

    echo ""
    echo "========================================================"
    echo "  Benchmarks completados"
    echo "========================================================"
    echo "  Resultados guardados en: $RESULTS_FILE"
    echo "========================================================"
    echo ""
}

# Ejecutar main y guardar resultados con tee
main | tee "$RESULTS_FILE"


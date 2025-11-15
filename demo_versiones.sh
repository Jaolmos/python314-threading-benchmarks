#!/bin/bash
# Script de demostracion: muestra como cambiar entre versiones

cd /home/jose/Escritorio/practica-programacion/python/rendimiento-python314

echo ""
echo "=========================================================="
echo "  DEMO: Cambiando entre versiones de Python con uv"
echo "=========================================================="
echo ""

echo ">>> Test 1: Python 3.12.3"
echo "Comando: uv run --python 3.12.3 test_version.py"
uv run --python 3.12.3 test_version.py

echo ""
echo ""

echo ">>> Test 2: Python 3.14.0 (con GIL)"
echo "Comando: uv run --python cpython-3.14.0-linux-x86_64-gnu test_version.py"
uv run --python cpython-3.14.0-linux-x86_64-gnu test_version.py

echo ""
echo ""

echo ">>> Test 3: Python 3.14.0t (sin GIL - freethreaded)"
echo "Comando: uv run --python cpython-3.14.0+freethreaded-linux-x86_64-gnu test_version.py"
uv run --python cpython-3.14.0+freethreaded-linux-x86_64-gnu test_version.py

echo ""
echo "=========================================================="
echo "  Como ves, cada comando usa una version diferente"
echo "  No hay que activar/desactivar nada"
echo "=========================================================="
echo ""


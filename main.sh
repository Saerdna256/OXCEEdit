#!/bin/bash

# Define environment and script paths
VENV_DIR=".venv"
PYTHON_SCRIPT="main.py"
PYTHON_CMD="${VENV_DIR}/bin/python"

# 1. Create virtual environment if it does not exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in ${VENV_DIR}..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Ensure pip is available in the venv
    if [ ! -f "${VENV_DIR}/bin/pip" ]; then
        echo "Installing pip in ${VENV_DIR}..."
        "${VENV_DIR}/bin/python" -m ensurepip --upgrade
    fi

    echo "Installing requirements from requirements.txt..."
    "${VENV_DIR}/bin/pip" install -r requirements.txt
fi

# 3. Run main.py using the virtual environment's Python interpreter
echo "Running ${PYTHON_SCRIPT}..."
exec "${PYTHON_CMD}" "${PYTHON_SCRIPT}" "$@"   
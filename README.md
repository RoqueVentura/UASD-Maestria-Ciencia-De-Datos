# INF-8239 · Unidad 01

Proyecto reproducible para INF-8239 Ciencia de Datos II (U01.LAB00).

## Entorno

- Sistema operativo: Windows 11 Pro (10.0.26200)
- Python: 3.10.11 (64 bits)
- Git: 2.53.0
- Editor: Visual Studio Code con Python, Jupyter, Pylance y Ruff

## Estructura

```
data/        datos (data/raw no se versiona)
notebooks/   cuadernos Jupyter
reports/     resultados e informes
src/         código fuente (paquete inf8239_u01)
tests/       pruebas unitarias
```

## Comandos usados (PowerShell)

```powershell
mkdir INF8239_U01
cd INF8239_U01
mkdir data notebooks reports src tests

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

$env:PYTHONPATH="src"
python -m pytest -q

git init
git add .
git commit -m "chore: create INF-8239 reproducible environment"
git status
git log --oneline
```

En macOS/Linux: `source .venv/bin/activate` y `PYTHONPATH=src python -m pytest -q`.

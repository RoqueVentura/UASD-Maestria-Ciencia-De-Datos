# INF-8239 · Unidad 01

Proyecto reproducible para INF-8239 Ciencia de Datos II: entorno (LAB00), SVM con pipeline sin fuga (LAB01), dataset propio con auditoría (LAB02) e informe del Ejercicio 01 (`reports/U01_E01_Roque_Ventura.pdf`).

## Entorno

- Sistema operativo: Windows 11 Pro (10.0.26200)
- Python: 3.10.11 (64 bits)
- Git: 2.53.0
- Editor: Visual Studio Code con Python, Jupyter, Pylance y Ruff

## Estructura

```
data/        datos (data/raw no se versiona)
docs/        ficha del dataset y diccionario de datos
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

## LAB02 · Dataset propio: HCV Data

- **Fuente:** UCI ML Repository, [HCV Data](https://archive.ics.uci.edu/dataset/571/hcv+data), CC BY 4.0, DOI 10.24432/C5D612. La procedencia, la licencia y la comparación de candidatos están en [docs/ficha_dataset.md](docs/ficha_dataset.md); el diccionario de datos, en [docs/diccionario_datos.md](docs/diccionario_datos.md).
- **Target:** `hepatopatia`, derivado de `Category`: `si` = hepatitis, fibrosis o cirrosis; `no` = donante sano. Se excluyen las filas `0s=suspect Blood Donor`, el identificador `Unnamed: 0` (fuga) y `Category` (fuente del target).
- **Métrica principal:** F1-macro, acompañada del recall de la clase `si`, porque el error más costoso es el falso negativo.

### Instalación

Sigue los pasos de "Comandos usados": crear `.venv` e instalar `requirements.txt`.

### Descarga

El CSV no se versiona (`data/raw/` está en `.gitignore`). Se descarga desde la URL pública de UCI a `data/raw/dataset.csv`:

```powershell
$env:PYTHONPATH="src"
python -c "from inf8239_u01.data import download_csv; download_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00571/hcvdat0.csv')"
```

La primera celda de descarga del notebook hace lo mismo.

### Ejecución

1. Abre `notebooks/02_dataset_propio.ipynb`, selecciona el kernel `.venv` y ejecuta **Run All**.
2. Ejecuta las pruebas. `tests/test_data_contract.py` requiere que el dataset ya esté descargado.

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

La conclusión está en [reports/conclusion_lab02.md](reports/conclusion_lab02.md).

from pathlib import Path
import pandas as pd

def download_csv(url: str, destination="data/raw/dataset.csv") -> Path:
    if not url.startswith(("https://", "http://")):
        raise ValueError("La fuente debe ser una URL HTTP(S)")
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(url)
    if frame.empty:
        raise ValueError("El dataset descargado está vacío")
    frame.to_csv(path, index=False)
    return path

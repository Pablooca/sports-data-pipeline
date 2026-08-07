"""Módulo de carga y persistencia de datos deportivos procesados."""

from pathlib import Path
import pandas as pd


def save_to_parquet(df: pd.DataFrame, output_path: str) -> Path:
    """Guarda un DataFrame en formato Parquet en la ruta especificada.

    Args:
        df (pd.DataFrame): DataFrame procesado a guardar.
        output_path (str): Ruta relativa o absoluta del archivo destino.

    Returns:
        Path: Objeto Path apuntando al archivo guardado.
    """
    if df.empty:
        raise ValueError("El DataFrame está vacío. No se guardará ningún archivo.")

    file_path = Path(output_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(file_path, index=False, engine="pyarrow")
    return file_path

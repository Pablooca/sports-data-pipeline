"""Tests unitarios para el módulo de carga de datos."""

from pathlib import Path
import pandas as pd
import pytest
from src.load import save_to_parquet


def test_save_to_parquet_success(tmp_path: Path):
    """Verifica que el DataFrame se guarde correctamente en formato Parquet."""
    sample_df = pd.DataFrame(
        [
            {
                "player": "Lionel Messi",
                "x_coord": 108.0,
                "y_coord": 40.0,
                "shot_statsbomb_xg": 0.75,
            }
        ]
    )

    output_file = tmp_path / "data" / "processed" / "shots.parquet"
    saved_path = save_to_parquet(sample_df, str(output_file))

    assert saved_path.exists()
    assert saved_path.suffix == ".parquet"

    # Cargar de nuevo para verificar que la integridad del contenido se mantiene
    loaded_df = pd.read_parquet(saved_path)
    assert len(loaded_df) == 1
    assert loaded_df["player"].iloc[0] == "Lionel Messi"


def test_save_to_parquet_empty_dataframe_raises_error(tmp_path: Path):
    """Verifica que se lance una excepción si se intenta guardar un DataFrame vacío."""
    empty_df = pd.DataFrame()
    output_file = tmp_path / "empty.parquet"

    with pytest.raises(
        ValueError, match="El DataFrame está vacío. No se guardará ningún archivo."
    ):
        save_to_parquet(empty_df, str(output_file))

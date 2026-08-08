"""Tests de integración para el orquestador del pipeline."""

from pathlib import Path
from unittest.mock import patch
import pandas as pd
from src.pipeline import run_shot_pipeline


@patch("src.pipeline.fetch_match_events")
def test_run_shot_pipeline_e2e(mock_fetch_events, tmp_path: Path):
    """Valida la ejecución del pipeline completo de principio a fin."""
    # Añadimos un tiro y un pase simulado para validar la Capa Gold completa
    mock_raw_data = pd.DataFrame(
        [
            {
                "id": "101",
                "type": "Shot",
                "team": "Argentina",
                "player": "Lionel Messi",
                "shot_statsbomb_xg": 0.85,
                "shot_outcome": "Goal",
                "location": [108.0, 40.0],
            },
            {
                "id": "102",
                "type": "Pass",
                "team": "Argentina",
                "player": "Lionel Messi",
                "pass_outcome": None,  # Pase completado
            },
        ]
    )
    mock_fetch_events.return_value = mock_raw_data

    output_file = tmp_path / "data" / "processed" / "test_gold_metrics.parquet"

    # Ejecutamos el pipeline
    result_path = run_shot_pipeline(match_id=3869685, output_path=str(output_file))

    assert result_path.exists()
    assert result_path.suffix == ".parquet"

    # Verificar que el archivo guardado tiene el esquema transformado de la Capa Gold
    processed_df = pd.read_parquet(result_path)

    assert len(processed_df) == 1
    assert "total_xg" in processed_df.columns
    assert "total_passes" in processed_df.columns

    # Validamos que las métricas de negocio se han calculado bien
    assert processed_df["player"].iloc[0] == "Lionel Messi"
    assert processed_df["total_xg"].iloc[0] == 0.85
    assert processed_df["total_passes"].iloc[0] == 1
    assert processed_df["successful_passes"].iloc[0] == 1
    assert processed_df["pass_accuracy_pct"].iloc[0] == 100.0

    mock_fetch_events.assert_called_once_with(3869685)

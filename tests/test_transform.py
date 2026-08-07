"""Tests unitarios para el módulo de transformación de datos."""

import pandas as pd
from src.transform import clean_shot_events


def test_clean_shot_events():
    """Valida el correcto filtrado y descomposicion de coordenadas en disparos."""
    raw_data = pd.DataFrame(
        [
            {
                "id": "1",
                "type": "Pass",
                "team": "Argentina",
                "player": "Messi",
                "location": [10.0, 20.0],
            },
            {
                "id": "2",
                "type": "Shot",
                "team": "Argentina",
                "player": "Messi",
                "shot_statsbomb_xg": 0.75,
                "shot_outcome": "Goal",
                "location": [108.0, 40.0],
            },
        ]
    )

    cleaned_df = clean_shot_events(raw_data)

    assert len(cleaned_df) == 1
    assert cleaned_df["player"].iloc[0] == "Messi"
    assert cleaned_df["shot_statsbomb_xg"].iloc[0] == 0.75
    assert cleaned_df["x_coord"].iloc[0] == 108.0
    assert cleaned_df["y_coord"].iloc[0] == 40.0

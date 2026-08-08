"""Tests unitarios para el módulo de agregación (Capa Gold)."""

import pandas as pd
from src.aggregate import create_player_metrics


def test_create_player_metrics_success():
    """Valida el cálculo de pases, % de acierto y xG sumado."""
    mock_events = pd.DataFrame(
        [
            # Pase completado de Messi (pass_outcome es nulo)
            {
                "id": "1",
                "type": "Pass",
                "team": "Argentina",
                "player": "Messi",
                "pass_outcome": None,
            },
            # Pase fallado de Messi (pass_outcome tiene valor)
            {
                "id": "2",
                "type": "Pass",
                "team": "Argentina",
                "player": "Messi",
                "pass_outcome": "Incomplete",
            },
            # Tiro de Messi con 0.5 xG
            {
                "id": "3",
                "type": "Shot",
                "team": "Argentina",
                "player": "Messi",
                "shot_statsbomb_xg": 0.5,
            },
            # Tiro de Messi con 0.3 xG
            {
                "id": "4",
                "type": "Shot",
                "team": "Argentina",
                "player": "Messi",
                "shot_statsbomb_xg": 0.3,
            },
            # Pase completado de Mbappé
            {
                "id": "5",
                "type": "Pass",
                "team": "France",
                "player": "Mbappé",
                "pass_outcome": None,
            },
        ]
    )

    gold_df = create_player_metrics(mock_events)

    assert not gold_df.empty
    assert len(gold_df) == 2  # Messi y Mbappé

    messi_stats = gold_df[gold_df["player"] == "Messi"].iloc[0]
    assert messi_stats["total_passes"] == 2
    assert messi_stats["successful_passes"] == 1
    assert messi_stats["pass_accuracy_pct"] == 50.0
    assert messi_stats["total_xg"] == 0.8  # 0.5 + 0.3

    mbappe_stats = gold_df[gold_df["player"] == "Mbappé"].iloc[0]
    assert mbappe_stats["total_passes"] == 1
    assert mbappe_stats["successful_passes"] == 1
    assert mbappe_stats["pass_accuracy_pct"] == 100.0
    assert mbappe_stats["total_xg"] == 0.0


def test_create_player_metrics_empty():
    """Valida el comportamiento con un DataFrame vacío."""
    empty_df = pd.DataFrame()
    result = create_player_metrics(empty_df)
    assert result.empty

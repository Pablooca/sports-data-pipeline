"""Tests unitarios para el módulo de extracción de datos."""

from unittest.mock import patch
import pandas as pd
from src.extract import fetch_match_events, get_free_competitions


@patch("src.extract.sb.competitions")
def test_get_free_competitions(mock_sb_competitions):
    """Verifica la llamadas al catálogo de competiciones de StatsBomb."""
    mock_df = pd.DataFrame(
        [{"competition_id": 43, "competition_name": "FIFA World Cup"}]
    )
    mock_sb_competitions.return_value = mock_df

    result = get_free_competitions()

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result["competition_name"].iloc[0] == "FIFA World Cup"
    mock_sb_competitions.assert_called_once()


@patch("src.extract.sb.events")
def test_fetch_match_events(mock_sb_events):
    """Verifica la extracción de eventos simulando la respuesta con un Mock."""
    mock_events_df = pd.DataFrame(
        [
            {
                "event_type": "Pass",
                "player": "Lionel Messi",
                "team": "Argentina",
            },
            {
                "event_type": "Shot",
                "player": "Kylian Mbappé",
                "team": "France",
            },
        ]
    )
    mock_sb_events.return_value = mock_events_df

    dummy_match_id = 3869685
    result = fetch_match_events(dummy_match_id)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "event_type" in result.columns
    mock_sb_events.assert_called_once_with(match_id=dummy_match_id)

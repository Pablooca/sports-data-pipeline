"""Módulo de transformación y limpieza de datos deportivos de StatsBomb."""

import pandas as pd


def clean_shot_events(df_events: pd.DataFrame) -> pd.DataFrame:
    """Filtra y limpia únicamente los eventos de tiros (Shots), extrayendo xG y coordenadas.

    Args:
        df_events (pd.DataFrame): DataFrame original de eventos de StatsBomb.

    Returns:
        pd.DataFrame: DataFrame procesado con información de tiros.
    """
    if df_events.empty or "type" not in df_events.columns:
        return pd.DataFrame()

    # Filtrar eventos cuyo tipo sea 'Shot'
    shots = df_events[df_events["type"] == "Shot"].copy()

    if shots.empty:
        return pd.DataFrame()

    # Seleccionar columnas clave si existen en el dataset
    expected_cols = [
        "id",
        "minute",
        "second",
        "team",
        "player",
        "shot_statsbomb_xg",
        "shot_outcome",
        "location",
    ]
    available_cols = [col for col in expected_cols if col in shots.columns]
    shots = shots[available_cols]

    # Descomponer las coordenadas [X, Y] de la columna 'location' en columnas separadas
    if "location" in shots.columns:
        shots["x_coord"] = shots["location"].apply(
            lambda loc: loc[0] if isinstance(loc, list) and len(loc) >= 2 else None
        )
        shots["y_coord"] = shots["location"].apply(
            lambda loc: loc[1] if isinstance(loc, list) and len(loc) >= 2 else None
        )
        shots = shots.drop(columns=["location"])

    return shots.reset_index(drop=True)

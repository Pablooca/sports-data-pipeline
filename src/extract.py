"""Módulo de extracción de datos deportivos utilizando StatsBomb API libre."""

import pandas as pd
from statsbombpy import sb


def get_free_competitions() -> pd.DataFrame:
    """
    Obtiene el catálogo de competiciones gratuitas disponibles en StatsBomb.

    Returns:
        pd.DataFrame: DataFrame con las competiciones disponibles.
    """
    competitions = sb.competitions()
    return competitions


def fetch_match_events(match_id: int) -> pd.DataFrame:
    """
    Extrae todos los eventos de un partido específico a través de su match_id.

    Args:
        match_id (int): Identificador único del partido en StatsBomb

    Returns:
        pd.DataFrame: DataFrame formateado con los eventos del encuentro
    """
    events = sb.events(match_id=match_id)
    return events


if __name__ == "__main__":
    # ID correspondiente a la final del Mundial de Qatar 2022 (Argentina vs Francia)
    WORLD_CUP_FINAL_ID = 3869685

    print("Cargando eventos de la final del Mundial 2022...")
    df_events = fetch_match_events(WORLD_CUP_FINAL_ID)
    print(
        f"Extracción exitosa:{len(df_events)} eventos cargados. "
        f"Columnas principales: {list(df_events.columns[:5])}"
    )

"""Módulo orquestador del pipeline ETL de datos deportivos."""

from pathlib import Path
from src.extract import fetch_match_events
from src.load import save_to_parquet
from src.transform import clean_shot_events


def run_shot_pipeline(match_id: int, output_path: str) -> Path:
    """
    Orquesta el flujo ETL completo para procesar tiros de un partido.

    Args:
        match_id (int): Identificador del partido en StatsBomb.
        output_path (str): Ruta donde se guardará el archivo Parquet resultante.

    Returns:
        Path: Ruta al archivo Parquet generado.
    """

    print(f"[1/3] Extrayendo eventos del partido {match_id}...")
    raw_events = fetch_match_events(match_id)

    print(f"[2/3] Transformando y limpiendo datos de tiros...")
    shots_df = clean_shot_events(raw_events)

    print(f"[3/3] Guardando resultado en {output_path}")
    saved_path = save_to_parquet(shots_df, output_path)

    print(" Pipeline ejecutado con éxito.")
    return saved_path


if __name__ == "__main__":
    # Final del Mundial de Qatar 2022 (Argentiva vs Francia)
    QATAR_FINAL_MATCH_ID = 3869685
    DESTINATION_FILE = "data/processed/qatar_2022_final_shots.parquet"

    run_shot_pipeline(match_id=QATAR_FINAL_MATCH_ID, output_path=DESTINATION_FILE)

"""Módulo orquestador del pipeline ETL de datos deportivos."""

import argparse
from pathlib import Path
from src.extract import fetch_match_events
from src.load import save_to_parquet
from src.transform import clean_shot_events
from src.aggregate import create_player_metrics


def run_shot_pipeline(match_id: int, output_path: str) -> Path:
    """Orquesta el flujo ETL completo para procesar eventos de un partido.

    Args:
        match_id (int): Identificador del partido en StatsBomb.
        output_path (str): Ruta base donde se guardarán los archivos Parquet.

    Returns:
        Path: Ruta al archivo Parquet generado de la Capa Gold.
    """
    print(f"[1/4] Extrayendo eventos crudos del partido {match_id} (Bronze)...")
    raw_events = fetch_match_events(match_id)

    print("[2/4] Transformando datos de tiros (Silver)...")
    shots_df = clean_shot_events(raw_events)
    silver_path = str(output_path).replace(".parquet", "_silver.parquet")
    save_to_parquet(shots_df, silver_path)

    print("[3/4] Generando métricas agregadas por jugador (Gold)...")
    gold_df = create_player_metrics(raw_events)

    print(f"[4/4] Guardando Capa Gold en {output_path}...")
    saved_path = save_to_parquet(gold_df, output_path)

    print("✅ Pipeline ejecutado con éxito.")
    return saved_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sports Data ETL Pipeline - StatsBomb Events Processing"
    )
    parser.add_argument(
        "--match-id",
        type=int,
        default=3869685,
        help="ID del partido en StatsBomb (por defecto: 3869685 - Final Mundial 2022)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/gold_metrics.parquet",
        help="Ruta del archivo Parquet de salida para la Capa Gold",
    )

    args = parser.parse_args()
    run_shot_pipeline(match_id=args.match_id, output_path=args.output)

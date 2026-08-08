import argparse
from pathlib import Path
from src.extract import fetch_match_events
from src.load import save_to_parquet
from src.transform import clean_shot_events


def run_shot_pipeline(match_id: int, output_path: str) -> Path:
    """Orquesta el flujo ETL completo para procesar tiros de un partido.

    Args:
        match_id (int): Identificador del partido en StatsBomb.
        output_path (str): Ruta donde se guardará el archivo Parquet resultante.

    Returns:
        Path: Ruta al archivo Parquet generado.
    """
    print(f"[1/3] Extrayendo eventos del partido {match_id}...")
    raw_events = fetch_match_events(match_id)

    print("[2/3] Transformando y limpiando datos de tiros...")
    shots_df = clean_shot_events(raw_events)

    print(f"[3/3] Guardando resultado en {output_path}...")
    saved_path = save_to_parquet(shots_df, output_path)

    print("Pipeline ejecutado con éxito.")
    return saved_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sports Data ETL Pipeline - StatsBomb Shot Events Processing"
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
        default="data/processed/shots.parquet",
        help="Ruta del archivo Parquet de salida",
    )

    args = parser.parse_args()
    run_shot_pipeline(match_id=args.match_id, output_path=args.output)

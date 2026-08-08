"""Módulo de la Capa Gold: Agregación de métricas de rendimiento por jugador."""

import pandas as pd


def create_player_metrics(df_events: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas agregadas de pases y xG por jugador a partir de los eventos.

    Args:
        df_events (pd.DataFrame): DataFrame con los eventos del partido.

    Returns:
        pd.DataFrame: DataFrame de la Capa Gold con las métricas por jugador.
    """
    if df_events.empty or "player" not in df_events.columns:
        return pd.DataFrame()

    # 1. Métricas de Pases
    passes = df_events[df_events["type"] == "Pass"].copy()

    if not passes.empty:
        # En StatsBomb, si 'pass_outcome' es nulo, el pase fue completado con éxito
        passes["is_successful"] = passes["pass_outcome"].isna()

        pass_stats = (
            passes.groupby(["team", "player"])
            .agg(
                total_passes=("id", "count"), successful_passes=("is_successful", "sum")
            )
            .reset_index()
        )

        pass_stats["pass_accuracy_pct"] = (
            (pass_stats["successful_passes"] / pass_stats["total_passes"]) * 100
        ).round(2)
    else:
        pass_stats = pd.DataFrame(
            columns=[
                "team",
                "player",
                "total_passes",
                "successful_passes",
                "pass_accuracy_pct",
            ]
        )

    # 2. Métricas de Tiros (xG)
    shots = df_events[df_events["type"] == "Shot"].copy()

    if not shots.empty and "shot_statsbomb_xg" in shots.columns:
        xg_stats = (
            shots.groupby(["team", "player"])
            .agg(total_xg=("shot_statsbomb_xg", "sum"))
            .reset_index()
        )
        xg_stats["total_xg"] = xg_stats["total_xg"].round(2)
    else:
        xg_stats = pd.DataFrame(columns=["team", "player", "total_xg"])

    # 3. Consolidar Capa Gold (Full Outer Join para no perder jugadores que solo tiraron o pasaron)
    if pass_stats.empty and xg_stats.empty:
        return pd.DataFrame()

    gold_metrics = pd.merge(
        pass_stats, xg_stats, on=["team", "player"], how="outer"
    ).fillna(0)

    # Ordenar por volumen de pases
    gold_metrics = gold_metrics.sort_values(by="total_passes", ascending=False)

    return gold_metrics.reset_index(drop=True)

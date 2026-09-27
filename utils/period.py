from datetime import date


MONTHS_FR = {
    1: "janvier",
    2: "février",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "août",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "décembre",
}


def calculate_period(exercice, trimestre):
    """
    Calcule automatiquement la période à partir de :

        Exercice : 2027
        Trimestre : T1 / T2 / T3 / T4

    Retourne une chaîne en français.
    """

    if exercice is None:
        return ""

    try:
        year = int(float(exercice))
    except (ValueError, TypeError):
        return ""

    if trimestre is None:
        return ""

    trimester = str(trimestre).strip().upper()

    periods = {
        "T1": (1, 1, 3, 31),
        "T2": (4, 1, 6, 30),
        "T3": (7, 1, 9, 30),
        "T4": (10, 1, 12, 31),
    }

    if trimester not in periods:
        return ""

    start_month, start_day, end_month, end_day = periods[
        trimester
    ]

    start_date = date(
        year,
        start_month,
        start_day
    )

    end_date = date(
        year,
        end_month,
        end_day
    )

    return (
        f"Du {start_date.day:02d} "
        f"{MONTHS_FR[start_date.month]} "
        f"{start_date.year} "
        f"au {end_date.day:02d} "
        f"{MONTHS_FR[end_date.month]} "
        f"{end_date.year}"
    )


def get_period_dates(exercice, trimestre):
    """
    Version structurée utile pour la future génération
    Word/PDF.
    """

    if exercice is None:
        return None

    try:
        year = int(float(exercice))
    except (ValueError, TypeError):
        return None

    trimester = str(
        trimestre or ""
    ).strip().upper()

    periods = {
        "T1": (1, 1, 3, 31),
        "T2": (4, 1, 6, 30),
        "T3": (7, 1, 9, 30),
        "T4": (10, 1, 12, 31),
    }

    if trimester not in periods:
        return None

    start_month, start_day, end_month, end_day = periods[
        trimester
    ]

    return {
        "start": date(
            year,
            start_month,
            start_day
        ),
        "end": date(
            year,
            end_month,
            end_day
        ),
        "label": calculate_period(
            year,
            trimester
        )
    }
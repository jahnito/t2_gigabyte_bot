

__all__ = ['calculate_coefficient']


def calculate_coefficient(lots: int,
                          rockets: int,
                          anomaly: int,
                          sold: int,
                          round_result: int = 3) -> float:
    all_lots = lots + rockets + anomaly
    if all_lots and sold:
        return round(sold / all_lots, round_result)
    elif sold and not all_lots:
        return sold
    else: # all_lots and not sold:
        return 0

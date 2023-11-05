def _clean_(x: str) -> str:
    return x.strip().lower().replace(',', '')


def parse_int(x) -> int:
    try:
        return int(_clean_(x))
    except ValueError:
        return None


def parse_float(x) -> float:
    try:
        return float(_clean_(x))
    except ValueError:
        return None

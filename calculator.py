MBG_PER_DAY = 1.2e12

def idr_to_mbg_days(idr_amount: float) -> float:
    return idr_amount / MBG_PER_DAY

def days_to_hours_minutes_seconds(days: float) -> tuple[int, int, float]:
    total_seconds = days * 24 * 60 * 60
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    return hours, minutes, seconds

def format_number(value: float, decimals: int = 8) -> str:
    if value > 1.0:
        decimals = 2
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

def parse_idr_input(text: str) -> float:
    clean = text.replace(".", "").replace(",", ".")
    try:
        return float(clean)
    except ValueError:
        return 0.0

def format_idr_input(text: str) -> str:
    clean = text.replace(".", "").replace(",", "")
    if clean.isdigit() and clean:
        return f"{int(clean):,}".replace(",", ".")
    return text

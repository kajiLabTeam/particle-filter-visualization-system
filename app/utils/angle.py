import secrets


def get_random_angle() -> float:
    return secrets.randbelow(361)


def reverse_angle(angle: float) -> float:
    return (angle + 180) % 360


def correction_angle(angle: float) -> float:
    return angle % 360


def turn_angle(angle: int) -> int:
    return -angle

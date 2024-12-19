import random


def get_random_angle() -> float:
    return random.randint(0, 360)


def reverse_angle(angle: float) -> float:
    return (angle + 180) % 360


def correction_angle(angle: float | int) -> float:
    return angle % 360


def turn_angle(angle: int) -> int:
    return -angle

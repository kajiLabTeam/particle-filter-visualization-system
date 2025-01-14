import random


def PARTICLES_STEP_ERROR() -> int:  # noqa: N802
    # 平均値0、標準偏差10の正規分布
    return int(random.gauss(0, 10))


def PARTICLES_ANGLE_ERROR() -> int:  # noqa: N802
    # 平均値0、標準偏差10の正規分布
    return int(random.gauss(0, 10))


def PARTICLES_DIRECTION_ERROR() -> float:  # noqa: N802
    import secrets

    return secrets.randbelow(181) - 90

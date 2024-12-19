import random
from controller import perform_particlefiltering_controller as perform_particlefiltering
from controller.perform_particlefiltering_controller import (
    get_particle_step_error_sd,
    get_particle_angle_error_sd,
)


def PARTICLES_STEP_ERROR() -> int:
    # 平均値0、標準偏差10の正規分布
    return int(random.gauss(0, get_particle_step_error_sd()))


def PARTICLES_ANGLE_ERROR() -> int:
    # 平均値0、標準偏差10の正規分布
    return int(random.gauss(0, get_particle_angle_error_sd()))


def PARTICLES_DIRECTION_ERROR() -> float:
    return random.randint(-90, 90)

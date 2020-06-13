from dataclasses import dataclass


@dataclass
class Config:
    FILE_NAME = None
    NUM_ITERATIONS = 3000

    ALPHA = 3
    BETA = 5
    RHO = 0.2

    USE_2_OPT_STRATEGY = True
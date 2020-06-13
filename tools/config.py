from dataclasses import dataclass


@dataclass
class Config:
    FILE_NAME = None
    NUM_ITERATIONS = 3000

    ALPHA = 3
    BETA = 5
    RHO = 0.25

    USE_2_OPT_STRATEGY = False
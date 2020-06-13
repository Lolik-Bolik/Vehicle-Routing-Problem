from dataclasses import dataclass


@dataclass
class Config:
    FILE_NAME = None
    NUM_ITERATIONS = 3000

    ALPHA = 0.3
    BETA = 0.5
    RHO = 0.05

    USE_2_OPT_STRATEGY = False
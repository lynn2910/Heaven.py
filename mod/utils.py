from typing import Tuple
from constants import *

# def fps_coeff(fps: int | float) -> float:
#     """
#     Renvoit un coefficient du nombre de mises à jours par secondes
#     le résultat sera toujours compris dans l'interval ]0; 1]
#     [!] Le résultat est automatiquement géré selon la constante `TICKS_PER_SECONDS`
#     """
#     coeff = float(fps) / UPDATE_TICKS
#     if coeff >= 1: return 1
#     else: return float(coeff)
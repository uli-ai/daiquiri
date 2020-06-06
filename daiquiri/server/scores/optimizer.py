# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import scipy

# =============================================================================
# MODULE FUNCTIONS
# =============================================================================
def hungarian(score):
    """ Find the match to maximize the score.

    """
    from scipy.optimize import linear_sum_assignment

    # get the row and column indices
    row, col = linear_sum_assignment(-score)

    return zip(row, col)

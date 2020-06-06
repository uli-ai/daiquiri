# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np

# =============================================================================
# MODULE FUNCTIONS
# =============================================================================
def sum_size_waste(donor_size, job_size):
    """ Match the sizes of job requests and donor restrictions.

    """
    if donor_size < job_size:
        return np.Inf

    else:
        return job_size - donor_size

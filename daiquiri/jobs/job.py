# =============================================================================
# IMPORTS
# =============================================================================
import abc

# =============================================================================
# MODULE CLASSES
# =============================================================================
class Job(abc.ABC):
    r""" Base class for all jobs.

    Job is one of the central objects of `daiquiri`. It is defined by
        * a step function which is the basic operation for a computation task
        * a data object that is (partly) fed into the step function during
          computation task
        * a state object that records the state of the computation. This is
          required to be able to be writen on disk and read to resume the
          computation.
        * a checkpoint function which periodically update the state.
        * a backend.

    The job object will be submitted by submittors as serialized object,
    cheked by server, and distributed to donors.

    Parameters
    ----------
    backend : str,
        the computation engine.

    Attributes
    ----------
    state : state of the computation.
    data : a generator-like object that feed data into `step`.

    Abstractmethods
    -------
    load : read the state and run/resume.
    step : conduct one step of computation.
    dump : called periodically, save checkpoints to disk.
    stop : terminate the computation and clean up.

    """
    def __init__(self, backend, state=None, data=None,
            step_idx=0, n_steps=1, dump_interval=1,
            *args, **kwargs):

        self.backend = backend
        self.state = state
        self.data = data
        self.step_idx = step_idx
        self.n_steps = n_steps
        self.dump_interval=dump_interval

    @abc.abstractmethod
    def load(self):
        """ Load state into computation task.

        Parameters
        ----------
        state_record : file-like object, contains the information
            to resume a computation.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self):
        """ Write state into a file.

        Parameters
        ----------
        state_record : file-like object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def step(self, *args, **kwargs):
        """ Basic step for a computation.

        """
        raise NotImplementedError

    def run(self):
        """ The method that should be universal for all jobs.

        """
        while self.step_idx < self.n_steps:
            self.step()
            if self.step_idx % self.dump_interval == 0:
                self.dump()

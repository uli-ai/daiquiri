# =============================================================================
# IMPORTS
# =============================================================================
import abc

# =============================================================================
# BASE CLASS
# =============================================================================
class Scheduler(abc.ABC):
    """ Base class for scheduler.

    """
    def __init__(self):
        super(Scheduler, self).__init__()

    @abc.abstractmethod
    def put(self, job):
        """ Put job to be scheduled.

        Parameters
        ----------
        job : `daiquiri.jobs.job.Job` object
            job that enters the scheduler.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, to):
        """ Get a job to be sent.

        Parameters
        ----------
        to : a representation of the donor machine spec.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, to, *args, **kwargs):
        """ Send job to donor. This interfaces with server connection
        facilities.

        Parameters
        ----------
        donor_address :
            the pointer to the donor.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def receive_job(self, from, *args, **kwargs):
        """ Receive a job.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def receive_donor(self, from, *args, **kwargs):
        """ Receive a donor.

        """
        raise NotImplementedError

    def schedule(self):
        """ Internal scheduling. Use graph matching algorithms to determine
        which job should go to which donor.

        """
        pass

# =============================================================================
# SCHEDULERS CLASSIFIED BY LOGIC
# =============================================================================
class QueueScheduler(Scheduler):
    """ Scheduler that schedules jobs on first-in, first-out basis.

    """
    def __init__(self, *args, **kwargs):
        super(QueueScheduler, self).__init__(*args, **kwargs)

        # init queue
        self.jobs = []
        self.donors = []

    def put(self, job):
        self.jobs.append(job)

    def get(self, job):
        return self.jobs[-1]

class ScoreScheduler(Scheduler):
    """ Scheduler that assigns jobs to maximize scores.

    """
    def __init__(self, score_fn, match_fn, *args, **kwargs):
        super(ScoreScheduler, self).__init__(*ars, **kwargs)

        self.score_fn = score_fn
        self.match_fn = match_fn
        self.jobs = []
        self.donors = []
        self.match = None

    def put(self, job):
        self.job.append(job)

    def get(self, to):
        if self.match is None:
            self.schedule()

        return self.match[to]

    def schedule(self):
        """ Schedule jobs to maximize some score.

        """
        # TODO:
        # consider vari-dimensional solution

        score = [
            score_fn(
                donor,
                job
            ) for donor in self.donors for job in self.jobs]

        self.match = self.match_fn(score)

# =============================================================================
# SCHEDULERS CLASSIFIED BY CONNECTION SPECS
# =============================================================================
class SocketScheduler(Scheduler):
    """ Scheduler that schedules jobs with socket.

    """
    def __init__(self, socket_agent, *args, **kwargs):
        super(SocketScheduler, self).__init__(*args, **kwargs)
        self.socket_agent = socket_agent

    def send(self, *args, **kwargs):
        self.socket_agent.send(*args, **kwargs)

    def receive(self, *args, **kwargs):
        self.socket_agent.receiv(*args, **kwargs)

# =============================================================================
# NON-ABSTRACT UTILITY SCHEDULERS
# =============================================================================
class SocketQueueScheduler(SocketScheduler, QueueScheduler):
    """ Scheduler that uses `QueueScheduler` for logistic and
    `SocketScheduler` for connection.

    """
    def __init__(self, socket_agent):
        super(SocketQueueScheduler).__init__(socket_agent=socket_agent)

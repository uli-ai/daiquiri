# =============================================================================
# IMPORTS
# =============================================================================
import abc
import daiquiri as dq
from dq.jobs.job import Job

# =============================================================================
# MODULE CLASSES
# =============================================================================
class TorchTrainJob(Job):
    """ Pytorch training job.
    
    """

    def __init__(self, data=None, model=None, optimizer=None, 
            **model_kwargs=None,
            **optimizer_kwargs=None):
        backend = 'torch'
        super(TorchTrainJob, self).__init__(
                backend)
        
        # we assume here that 
        #  * a training is only dependent on data, model,
        #    and optimizer
        #  * what is fed into this object is only unintialized
        #    model and optiizer
        self.model = model()
        self.optimizer = optimizer(
                model.parameters(),
                **optimizer_kwargs)

        self.step_idx = 0
        self.epoch_idx = 0

        # we only do import here to support the donors
        # without torch installed
        import torch

        # TODO:
        # version control

    def load(self, state_record, optimizer_state_record):
        """ Load state dicts into model and optimizer.

        """ 
        
        self.model.load_state_dict(
            torch.load(state_record))

        self.optimizer.load_state_dict(
            torch.load(optimizer_state_record))

    def step(self):
        """ Do one step of training.

        """
        # empty variable grad
        self.optimizer.zero_grad()

        # get data
        data = next(self.data)

        # feed data into model to get loss function
        # here we of course assume forward function
        # only gives loss
        loss = self.model(*data)

        # further assume that data is already with grad
        # which is most of the time true
        loss.backward()
        self.optimizer.step()

        self.step_idx += 1
        
        # TODO:
        # implement mechanisms for multiple epochs

    def dump(self, state_record, optimizer_state_record, 
            job_state_record):

        self.model.save_state_dict(state_record)
        self.optimizer.save_state_dict(optimizer_state_record)
        
        # TODO:
        # implement mechanisms to write basis step indices
        # into a file
        






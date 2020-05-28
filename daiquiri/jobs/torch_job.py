# =============================================================================
# IMPORTS
# =============================================================================
import abc
import daiquiri as dq
from daiquiri.jobs.job import Job

# =============================================================================
# MODULE CLASSES
# =============================================================================
class TorchTrainJob(Job):
    """ Pytorch training job.

    Parameters
    ----------
    data : a iterable or `torch.utils.data.DataLoader` object.
        dataset on which a model is being trained.
    model : a `torch.nn.Module` object.
        a model that holds parameters.
    optimizer : a `torch.optim.Optimizer` object.
        optimizer which tunes the parameters.
    kwargs : arguments for optimizer and model.
        note that keyword for optimizer has to start with '_optimizer_',
        and keyword for model has to start with '_model_'

    Methods
    -------

    """

    def __init__(self, model, optimizer,
            backend='torch',
            state=None, data=None,
            loss_fn='mse_loss', # TODO: replace, it's ugly
            step_idx=0, n_steps=1, dump_interval=1,
            model_state_dict_path='model.th',
            optimizer_state_dict_path='optimizer.th',
            *args, **kwargs):

        # split model and optimizer keword args
        model_kwargs = {key: value for key, value in kwargs.items()
            if key.startswith('_model_')}

        optimizer_kwargs = {key: value for key, value in kwargs.items()
            if key.startswith('_optimizer_')}

        # we assume here that
        #  * a training is only dependent on data, model,
        #    and optimizer
        #  * what is fed into this object is only unintialized
        #    model and optiizer
        self.model = model(**model_kwargs)
        self.optimizer = optimizer(
                self.model.parameters(),
                **optimizer_kwargs)

        self.model_state_dict_path = model_state_dict_path
        self.optimizer_state_dict_path = optimizer_state_dict_path

        self.data = data


        # NOTE: here we assume that
        # one epoch is one step
        # because the shuffling of the dataset might be different
        # and not all the `data` object has `__get__` method  implemented

        # TODO:
        # implement a separate `step_within_epoch` to support pause
        # within epch

        # we only do import here to support the donors
        # without torch installed
        import torch
        self.loss_fn = getattr(torch.nn.functional, loss_fn)

        super(TorchTrainJob, self).__init__(
                backend=backend,
                data=data)

        # TODO:
        # version control

    def load(self):
        """ Load state dicts into model and optimizer.

        """
        import torch

        self.model.load_state_dict(state_dict)
        self.optimizer.load_state_dict(
            torch.load(self.optimizer_state_dict_path))


    def step(self):
        """ Train for an entire episode.

        Note
        ----
        We should add support for training on minibatches soon.


        """
        # TODO:
        # more general grammar
        for x, y in self.data: # `data` object should support this grammar

            # empty variable grad
            self.optimizer.zero_grad()

            # feed data into model to get loss function
            # here we of course assume forward function
            # only gives loss
            y_hat = self.model(x)
            loss = self.loss_fn(y, y_hat)

            # further assume that data is already with grad
            # which is most of the time true
            loss.backward()
            self.optimizer.step()


    def dump(self):
        import torch
        torch.save(self.model.state_dict(), self.model_state_dict_path)
        torch.save(self.optimizer.state_dict(), self.optimizer_state_dict_path)

        # TODO:
        # implement mechanisms to write basis step indices
        # into a file

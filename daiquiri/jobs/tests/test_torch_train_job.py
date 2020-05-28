import pytest
import torch
import numpy as np
import math

@pytest.fixture
def data():
    # sinusoidal toy data
    f = lambda x: torch.sin(x)

    x_tr = torch.tensor(np.concatenate(
        [
            np.linspace(-3 * math.pi, -math.pi, 50),
            np.linspace(math.pi, 3 * math.pi, 50)
        ]),
        dtype=torch.float32)[:, None]

    y_tr = f(x_tr)

    # let's have two epochs!
    return [[x_tr, y_tr], [x_tr, y_tr]]

@pytest.fixture
def model():
    # note that model has to be a callable!
    net = lambda: torch.nn.Sequential(
        torch.nn.Linear(1, 50),
        torch.nn.Tanh(),
        torch.nn.Linear(50, 1))

    return net

@pytest.fixture
def optimizer():
    return torch.optim.Adam

def test_import():
    import daiquiri as dq
    import daiquiri.jobs.torch_job


def test_init(model, data, optimizer):
    import daiquiri as dq

    torch_job = dq.jobs.torch_job.TorchTrainJob(
        model=model,
        data=data,
        optimizer=optimizer)

@pytest.fixture
def job(model, data, optimizer):
    import daiquiri as dq

    torch_job = dq.jobs.torch_job.TorchTrainJob(
        model=model,
        data=data,
        optimizer=optimizer)
    return torch_job

def test_step(job):
    job.step()

def test_dump(job):
    job.dump()

def test_dump_and_load(job):
    job.dump()
    job.load()

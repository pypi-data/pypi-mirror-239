import numpy as np
from nnabla.initializer import NormalInitializer, UniformInitializer


def torch_initializer(inmaps, kernel):
    d = np.sqrt(1. / (kernel * kernel * inmaps))
    return UniformInitializer((-d, d))


def he_initializer(ochan, kernel, rng):
    return NormalInitializer(
        sigma=np.sqrt(2 / (kernel * kernel * ochan)),
        rng=rng
    )


def bilinear_depthwise_initializer(ichan, kernel):
    factor = (kernel + 1) // 2
    if kernel % 2 == 1:
        center = factor - 1
    else:
        center = factor - 0.5
    og = (np.arange(kernel).reshape(-1, 1), np.arange(kernel).reshape(1, -1))
    filt = (1 - np.abs(og[0] - center) / factor) * \
        (1 - np.abs(og[1] - center) / factor)
    weight = np.zeros((ichan, kernel, kernel))
    weight = np.broadcast_to(filt, (ichan, kernel, kernel))
    weight = np.expand_dims(weight, axis=1)
    return np.array(weight)


def bilinear_initializer(ichan, kernel):
    factor = (kernel + 1) // 2
    if kernel % 2 == 1:
        center = factor - 1
    else:
        center = factor - 0.5
    og = (np.arange(kernel).reshape(-1, 1), np.arange(kernel).reshape(1, -1))
    filt = (1 - np.abs(og[0] - center) / factor) * \
        (1 - np.abs(og[1] - center) / factor)
    weight = np.zeros((ichan, ichan, kernel, kernel))
    for i in range(ichan):
        weight[i, i] = filt
    return np.array(weight)

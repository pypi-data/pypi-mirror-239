import torch
import numpy as np
import random
def set_seed(seed=3) -> None:
    """set seed for module included numpy torch and standard library random default to seed.

    Args:
        seed (int, optional): the seed to set. Defaults to 3.
    """    
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

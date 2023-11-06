from __future__ import annotations
from typing import Any
import numpy as np
import numpy
import torch

Vector = Any


class Spsa():
    ''''own the grad_calcu, initial_hyperparameters, update_parameters method to update parameter'''

    def __init__(self) -> None:
        pass


    def initial_hyperparameters(self,
                                alpha: float,
                                lossFunction: Any,
                                w0: torch.Tensor | numpy.ndarray,
                                N_iterations: int,
                                c: float = 0.5,
                                delta_wi: float = 0.009) -> tuple[float, ...]:
        """ the method to initial parameter.


        Args:
            alpha (float): 
            lossFunction (Any): Control the attenuation of learning rate.
            w0 (torch.Tensor  |  numpy.ndarray): initial parameter.
            N_iterations (int):the number for updating parameter.  
            c (float, optional): perturbation for the parameter. Defaults to 0.5.
            delta_wi (float, optional): the perturbation amplitude for the first few parameter . Defaults to 0.009.

        Returns:
            tuple[float, ...]:the computed hyperparameters for updating parameters
        """
        A = N_iterations * 0.1  #0.92
        # order of magnitude of first gradients
        magnitude_g0 = np.abs(self.grad_calcu(lossFunction, w0, c).mean())
        a = delta_wi * (
            (A + 1)**alpha) / magnitude_g0  #1.9**0.8=1.67  delta_wi 起开振幅
        return a, A, c
    def grad_calcu(self, L: Any, w: torch.Tensor | numpy.ndarray,
                   ck: float | int) -> float:
        """the method to approximate calculate parameter.

        Args:
            L (Any): the lossfunction passed in.
            w (torch.Tensor  |  numpy.ndarray): parameter in circuit.
            ck (float | int): the perturbation factor for parameter.

        Returns:
            float: the gradent loss correspondding to parameter.
        """
        p = len(w)
        # bernoulli-like distribution
        deltak = np.random.choice([-1, 1], size=p)
        ck_deltak = ck * deltak
        # gradient approximation
        l_pos, _ = L(w + ck_deltak)
        l_neg, _ = L(w - ck_deltak)
        DELTA_L = l_pos - l_neg
        return (DELTA_L) / (2 * ck_deltak)

    def update_parameters(self,
                          k: int,
                          lossfunction: Any,
                          parameters: torch.Tensor | numpy.ndarray,
                          a: float,
                          A: float | int,
                          c: float | int,
                          alpha: float = 0.8,
                          gamma: float | int = 0.101) -> Vector:
        """ the method to update parameter.


        Args:
            k (int): parameter update times.
            lossfunction (Any): lossfunction used for computing gradient.
            parameters (torch.Tensor  |  numpy.ndarray]): parameters be updated.
            a (float): hyperparameters.
            A (float | int): hyperparameters.
            c (float | int): hyperparameters.
            alpha (float, optional): hyperparameters. Defaults to 0.8.
            gamma (float | int, optional): hyperparameters. Defaults to 0.101.

        Returns:
            Vector: new hyperparameters
        """
        ak = a / ((k + A)**(alpha))  #lr
        ck = c / (k**(gamma))  #delta
        # estimate gradient
        gk = self.grad_calcu(L=lossfunction, w=parameters, ck=ck)  #ndarray
        gk = torch.tensor(gk)
        # update parameters
        # print(f'a: {a}--ak*gk:{ak*gk}')
        parameters -= ak * gk
        return parameters

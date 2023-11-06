from __future__ import annotations
import random
from typing import Any
import torch
from torch.utils import data
from isqtools import IsqCircuit
from isqtools.backend import TorchBackend
from easydict import EasyDict
import os
import pathlib
import numpy
import numpy as np
from ..sto_optimizer import Spsa

Vector = Any


class Train_data():
    flags = EasyDict({
        'seed': 3,
        'total_params': 27,
        'qbit_num': 8,
        'batch_size_train': 100,
        'learning_rate': 0.01,
        'alpha': 0.8,
        'gamma': 0.101,
        'epoch': 1,
        'device': 'cpu'
    })

    def __init__(self,
                 opti_accu: int | float = 0,
                 opti_parameter: torch.Tensor | numpy.ndarray = None) -> None:
        """
        class attribute:
        flags: class attribute own default value, you can change the default value by youself.
        flags = EasyDict({
        'seed': 3,
        'total_params': 27,
        'qbit_num': 8,
        'batch_size_train': 100,
        'learning_rate': 0.01,
        'opti_accu': 0,
        'opti_parameter': 0,
        'alpha': 0.8,
        'gamma': 0.101,
        'epoch': 1,
        'device': 'cpu'
        })
            Args:
            opti_accu (int | float, optional): initial optimal accuracy of the module. Defaults to 0.
            opti_parameter (torch.Tensor | numpy.ndarray, optional): optimal  parameter of the module. Defaults to None.
        """
        self.opti_accu = opti_accu
        self.opti_parameter = opti_parameter
        self.optimazer = Spsa()



    def load_array(self,
                   data_arrays: tuple[torch.Tensor | numpy.ndarray,
                                      torch.Tensor | numpy.ndarray],
                   batch_size: int,
                   generator: Any,
                   shuffle: bool = True) -> Vector:
        """construct a torch data loader.

        Args:
            data_arrays (tuple[torch.Tensor|numpy.ndarray,torch.Tensor|numpy.ndarray]): the data to be wrapped to torch dataloader.
            batch_size (int): batch size setted
            shuffle (bool, optional): if to shuffle the data. Defaults to True.

        Returns:
            Vector: return a torch dataloader for iteration.
        """
        dataset = data.TensorDataset(*data_arrays)
        return data.DataLoader(dataset,
                               batch_size,
                               drop_last=True,
                               generator=generator,
                               shuffle=shuffle)

    def circuit_module(
        self,
        isq_file: str = os.path.join(
            str(pathlib.Path(__file__).resolve().parents[1]), 'isq_nn',
            'device_circuit8.isq'),
        backend: Any = TorchBackend()
    ) -> Any:
        """construct a circuit module based isq.

        Args:
            isq_file (str, optional): the location of isq file. Defaults to 'device_circuit8.isq'.
            backend (Any, optional): choose the backend to execute. Defaults to TorchBackend().

        Returns:
            Any: a circuit module based isq acceptted inputs and weights correspondding to module.
        """

        qc = IsqCircuit(
            file=isq_file,
            backend=backend,
            sample=False,
            int_param=[self.flags.total_params, self.flags.qbit_num])

        def circuit(inputs, weights):
            result = qc.pauli_measure(inputs=inputs, weights=weights)
            return result

        vcircuit = torch.vmap(circuit, in_dims=(0, None))
        if isinstance(backend, TorchBackend):
            return vcircuit
        else:
            return circuit
    def test(self, x_test: torch.Tensor | numpy.ndarray,
             y_test: torch.Tensor | numpy.ndarray,
             parameters: torch.Tensor | numpy.ndarray,
             circuit) -> Vector:
        """test  module

        Args:
            x_test (torch.Tensor | numpy.ndarray): the data feature for test.
            y_test (torch.Tensor | numpy.ndarray): the data label for test.
            parameters (torch.Tensor | numpy.ndarray): the weights of module.
            circuit(Any):circuit module.

        Returns:
            Vector:accuracy, preb.
            accuracy:  the test accuracy.
            pred: the result for module prediction.
        """
        test_loss, pred = self.lossfun_calcu(parameters, x_test, y_test,circuit)
        #
        pred = torch.where(pred < 0, 0., 1.)
        com = (pred == y_test).type(torch.float).sum().item()
        accuracy = com / len(x_test)
        print(
            f"Test Error: \n Accuracy: {(100*accuracy):>0.1f}%, Avg loss: {test_loss:>8f} \n"
        )
        return accuracy, pred

    def lossfun_calcu(self,
                      parameters: torch.Tensor | numpy.ndarray,
                      x_data: torch.Tensor | numpy.ndarray,
                      y_data: torch.Tensor | numpy.ndarray,
                      circuit:Any,
                      device: bool = False) -> tuple[float, Any]:
        """_summary_

        Args:
            parameters (torch.Tensor | numpy.ndarray): the parameters used to update.
            x_data (torch.Tensor | numpy.ndarray): train data.
            y_data (torch.Tensor | numpy.ndarray): train label.
            circuit(Any):circuit module.
            device (bool, optional): what kind of backend is used to execute circuit. Defaults to False.

        Returns:
            tuple[float, Any]: the loss between the prediction value return by circuit and data label.
        """
        if device == True:
            pred = []
            for i in range(len(x_data)):
                pred.append(circuit(x_data[i], parameters))
        else:
            pred = circuit(x_data, parameters)
        pred = torch.tensor(pred)
        L = torch.nn.functional.binary_cross_entropy_with_logits(
            pred, y_data).item()
        return L, pred

    def train_module(
        self,
        x_train: torch.Tensor | numpy.ndarray,
        x_test: torch.Tensor | numpy.ndarray,
        y_train: torch.Tensor | numpy.ndarray,
        y_test: torch.Tensor | numpy.ndarray,
        parameters: torch.Tensor | numpy.ndarray,
        set_default_hyper_param: tuple[int | float, int | float,
                                       int | float] = []
    ) -> tuple[torch.Tensor | numpy.ndarray, float | int]:
        """train and module return optimal parameter and accuracy.

        Args:
            x_train (torch.Tensor | numpy.ndarray): the data feature used to train modle.
            x_test (torch.Tensor | numpy.ndarray): the data feature used to test modle.
            y_train (torch.Tensor | numpy.ndarray): the label according to x_train.
            y_test (torch.Tensor | numpy.ndarray): label according to x_test.
            parameters(torch.Tensor | numpy.ndarray): parameters to be updated.initial parameter default generated by torch.
            set_default_hyper_param (tuple[int  |  float, int  |  float, int  |  float], optional): set customized a,A,c hyperparameter. Defaults to [].

        Returns:
            tuple[torch.Tensor | numpy.ndarray,float|int]: 
            self.opti_parameter: optimal weights found.
            self.opti_accu: optimal accuracy found.
        """
        if self.flags.device == 'cpu':
            generator = None
        else:
            generator = torch.Generator(device='cuda')

        train_dataloader = self.load_array(
            (x_train, y_train),  #11620
            batch_size=self.flags.batch_size_train,
            generator=generator)
        circuit=self.circuit_module()
        train_batchnum = int(len(x_train) / self.flags.batch_size_train)
        for e in range(0, self.flags.epoch):
            print(f"Epoch {e+1}\n-------------------------------")
            for batch, (X, y) in enumerate(train_dataloader):
                lossFunction = lambda parameters: self.lossfun_calcu(
                    parameters, X, y,circuit)
                if set_default_hyper_param:
                    a, A, c = set_default_hyper_param
                elif batch == 0:
                    a, A, c = self.optimazer.initial_hyperparameters(
                        self.flags.alpha, lossFunction, parameters,
                        (e + 1) * train_batchnum)
                parameters = self.optimazer.update_parameters(
                    e * train_batchnum + batch + 1, lossFunction, parameters,
                    a, A, c, self.flags.alpha, self.flags.gamma)
                print(f"batch------{batch+1}")
                accuracy, pred = self.test(x_test, y_test, parameters,circuit)
                if accuracy > self.opti_accu:
                    self.opti_accu = accuracy
                    self.opti_parameter = parameters
        print('train end'.title(),
              f'\n----optimal accuracy is {self.opti_accu}')
        return self.opti_parameter, self.opti_accu

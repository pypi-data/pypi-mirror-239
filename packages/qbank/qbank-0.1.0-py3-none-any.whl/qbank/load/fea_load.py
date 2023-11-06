from __future__ import annotations
from typing import Any
import pandas as pd
import numpy as np
import numpy
import os
import torch

Vector = Any


class Fload():
    """load, deal, split the dataset.
       map_dict: mapping the different string item which is the key of supplied dict existed in dataset to value in dict.
       
       Method:
       __init__():
       data_load:load the data form csv file(included one file own both train and test data or two file included.
    """

    map_dict = {
        "admin.": 1.,
        "unknown": 2.,
        "unemployed": 3.,
        "management": 4.,
        "housemaid": 5.,
        "entrepreneur": 6.,
        "student": 7.,
        "blue-collar": 8.,
        "self-employed": 9.,
        "retired": 10.,
        "technician": 11.,
        "services": 12.,
        "married": 1,
        "divorced": 2,
        "single": 3,
        "unknown": 1,
        "secondary": 2,
        "primary": 3,
        "tertiary": 4,
        "yes": 1,
        "no": 0,
        "unknown": 1,
        "telephone": 2,
        "cellular": 3,
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
        "unknown": 1,
        "other": 2,
        "failure": 3,
        "success": 4
    }

    def __init__(self) -> None:
        pass

    def featu_change(self, arr: numpy.ndarray) -> numpy.ndarray:
        """mapping the different string item which is the key of supplied dict to value in dict. 

        Args:
            arr (numpy.ndarray): the array will to be dealed.

        Returns:
            numpy.ndarray: the array dealed.
        Examples
        -------
        map_dic={
        "yes":1,"no":0,"jan":2, "feb":3, "mar":4, "apr":5
        }
        arr=np.array([['yes', 'no'],
            ['jan', 'feb'],
            ['mar', 'apr'],
            ])
        >>> fload.featu_change(arr)
        [['1' '0']
        ['2' '3']
        ['4' '5']]
         """
        for k, v in self.map_dict.items():
            arr[np.where(arr == k)] = v
        return arr

    def normalize(self, date: numpy.ndarray) -> numpy.ndarray:
        """normalize the item in array [0,1] by column.
        
        Args:
            date (numpy.ndarray): array to normalize

        Returns:
            numpy.ndarray: normalized array
        Examples
        -------
        >>> np.array([[4, 20],
            [1, 3],
            [5, 5],
            ])
        >>> fload.normalize(data)
        [[0.75       1.        ]
        [0.         0.        ]
        [1.         0.11764706]]        
        """
        vmax = np.max(date, axis=0)
        vmin = np.min(date, axis=0)
        dev = vmax - vmin
        date = (date - vmin) / dev
        return date

    def data_load(self,
                  f_position: str,
                  f_name: str | list = ['train.csv', 'test.csv'],
                  featu_dim: int = 16) -> Vector:
        """ load the data form csv file, included one file own both train and test data or two file separately.

        Args:
            f_position (str): the location data to load unincluded the filename. 
            f_name (str | list, optional): filename of the data file, either only one file included all data or two
            file included train and test file Defaults to ['train.csv','test.csv'].
            featu_dim (int, optional): tran data dim. Defaults to 16.

        Returns:
            Vector: 
                    x_train,x_test,x_vali(torch.Tensor): train test vali data feature splited.
                    y_train,y_test,y_vali(torch.Tensor): label correspondding to  train test vali data.   
                    len_featu(int): the size of dataset.
        """
        if type(f_name) == list:
            df_train = pd.read_csv(os.path.join(f_position, f_name[0]),
                                   sep=';')
            df_test = pd.read_csv(os.path.join(f_position, f_name[1]), sep=';')
            featu_train = np.asarray(df_train)
            featu_test = np.asarray(df_test)
            featu = np.concatenate((featu_train, featu_test), axis=0)
        else:
            df_dataset = pd.read_csv(os.path.join(f_position, f_name), sep=';')
            featu = np.asarray(df_dataset)

        featu_y = featu[featu[:, featu_dim] == 'yes', :]
        featu_n = featu[featu[:, featu_dim] == 'no', :]
        featu_n = featu_n[np.random.choice(len(featu_n),
                                           size=len(featu_y),
                                           replace=False)]
        featu_dealed = np.concatenate((featu_n, featu_y), axis=0)
        np.random.shuffle(featu_dealed)
        len_featu = len(featu_dealed)
        featu_dealed = self.featu_change(featu_dealed).astype(np.float32)
        featu_dealed = self.normalize(featu_dealed)
        x_featu, y_featu = np.split(featu_dealed, [featu_dim], axis=1)
        y_featu = y_featu.flatten()
        x_train = x_featu[:int(0.8 * len_featu)]
        x_test = x_featu[int(0.8 * len_featu):int(0.8 * len_featu) +
                         int(0.1 * len_featu)]
        x_vali = x_featu[int(0.8 * len_featu) +
                         int(0.1 * len_featu):int(0.8 * len_featu) +
                         int(0.2 * len_featu)]
        y_train = y_featu[:int(0.8 * len_featu)]
        y_test = y_featu[int(0.8 * len_featu):int(0.8 * len_featu) +
                         int(0.1 * len_featu)]
        y_vali = y_featu[int(0.8 * len_featu) +
                         int(0.1 * len_featu):int(0.8 * len_featu) +
                         int(0.2 * len_featu)]

        x_train = torch.from_numpy(x_train)
        y_train = torch.from_numpy(y_train)
        x_test = torch.from_numpy(x_test)
        y_test = torch.from_numpy(y_test)
        x_vali = torch.from_numpy(x_vali)
        y_vali = torch.from_numpy(y_vali)
        return x_train, x_test, x_vali, y_train, y_test, y_vali, len_featu

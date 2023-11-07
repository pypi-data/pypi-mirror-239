from typing import Union, List
import numpy as np
import pandas as pd


class TimeSplitter:
    def __init__(self, train_size: int, test_size: int, gap: int = 0, return_pandas: bool = False):
        """
        Inicializa o objeto TimeSplitter com tamanhos de treinamento e teste, e um intervalo (gap) opcional.

        Args:
            train_size (int): O tamanho do conjunto de treinamento em cada divisão.
            test_size (int): O tamanho do conjunto de teste em cada divisão.
            gap (int, opcional): O intervalo entre os conjuntos de treinamento e teste em cada divisão.
                O valor padrão é 0.
            return_pandas: bool: Indica que o splitter retornará uma lista de dataframes quando aplicável
        """
        self.train_size = train_size
        self.test_size = test_size
        self.gap = gap
        self.return_pandas = return_pandas
        self.fold_size = self.train_size + self.gap + self.test_size

    def split(
        self, X: Union[np.ndarray, pd.DataFrame]
    ) -> Union[np.ndarray, List[pd.DataFrame]]:
        """
        Divide a série temporal em conjuntos de treinamento e teste.

        Args:
            X (numpy.ndarray ou pandas.DataFrame): A série temporal a ser dividida.

        Returns:
            train_datasets (Union[np.ndarray, List[pd.DataFrame]]): Uma lista de conjuntos de treinamento.
            test_datasets (Union[np.ndarray, List[pd.DataFrame]]): Uma lista de conjuntos de teste.
        """
        data_type = "numpy"
        if isinstance(X, pd.DataFrame):
            data_type = "pandas"
        n, *_ = X.shape
        n_splits = n - self.fold_size + 1
        train_datasets = self._get_train_datasets(X, n_splits, data_type)
        test_datasets = self._get_test_datasets(X, n_splits, data_type)
        return train_datasets, test_datasets

    def _get_train_datasets(
        self, X: Union[pd.DataFrame, np.ndarray], n_splits: int, data_type: str
    ) -> Union[np.ndarray, List[pd.DataFrame]]:
        datasets = [self._get_train_slice(X, i, data_type) for i in range(n_splits)]
        if (data_type != "pandas") or (not self.return_pandas):
            datasets = np.array(datasets)
        return datasets

    def _get_test_datasets(
        self, X: Union[pd.DataFrame, np.ndarray], n_splits: int, data_type: str
    ) -> Union[np.ndarray, List[pd.DataFrame]]:
        datasets = [self._get_test_slice(X, i, data_type) for i in range(n_splits)]
        if (data_type != "pandas") or (not self.return_pandas):
            datasets = np.array(datasets)
        return datasets

    def _get_slice(
        self, df: Union[pd.DataFrame, np.ndarray], start: int, end: int, data_type: str
    ) -> Union[pd.DataFrame, np.ndarray]:
        if data_type == "pandas":
            return df.iloc[start:end]
        return df[start:end]

    def _get_train_slice(
        self, X: Union[pd.DataFrame, np.ndarray], i: int, data_type: str
    ) -> Union[pd.DataFrame, np.ndarray]:
        return self._get_slice(X, i, i + self.train_size, data_type)

    def _get_test_slice(
        self, X: Union[pd.DataFrame, np.ndarray], i: int, data_type: str
    ) -> Union[pd.DataFrame, np.ndarray]:
        return self._get_slice(
            X,
            i + self.train_size + self.gap,
            i + self.train_size + self.gap + self.test_size,
            data_type,
        )

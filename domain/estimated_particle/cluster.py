from typing import List

import numpy as np
from numpy.typing import NDArray
from scipy import stats
from sklearn.cluster import KMeans


class Cluster:
    @staticmethod
    def build(X: NDArray, k_means: KMeans, index=None) -> List["Cluster"]:
        if index is None:
            index = np.arange(X.shape[0])

        clusters = [
            Cluster(X, index, k_means, label)
            for label in range(k_means.get_params()["n_clusters"])
        ]

        return clusters

    def __init__(
        self,
        X: NDArray,
        index: NDArray,
        k_means: KMeans,
        label: int,
    ):
        self.data: NDArray = X[k_means.labels_ == label]
        self.index = index[k_means.labels_ == label]
        self.size = self.data.shape[0]
        self.df = self.data.shape[1] * (self.data.shape[1] + 3) / 2
        self.center = k_means.cluster_centers_[label]

        if self.size > 1:
            self.cov = np.cov(self.data.T)
            # Check for singular matrix and adjust if necessary
            if np.linalg.matrix_rank(self.cov) < self.cov.shape[0]:
                self.cov += (
                    np.eye(self.cov.shape[0]) * 1e-6
                )  # Adding a small value to diagonal
        else:
            self.cov = np.eye(self.data.shape[1]) * 1e-6

    def log_likelihood(self) -> float:
        self.data = np.array(
            [x for x in self.data if not (np.isnan(x).any() or np.isinf(x).any())]
        )
        if len(self.data) == 0:
            return -np.inf

        log_likelihoods = [
            stats.multivariate_normal.logpdf(
                x, self.center, self.cov, allow_singular=True
            )
            for x in self.data
        ]
        return sum(log_likelihoods)

    def bic(self):
        return -2 * self.log_likelihood() + self.df * np.log(self.size)

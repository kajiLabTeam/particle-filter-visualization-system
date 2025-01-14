import numpy as np
from numpy.typing import NDArray
from scipy import stats
from sklearn.cluster import KMeans

from app.domain.estimated_particle.cluster import Cluster


class ConvergenceJudgment:
    def __init__(self, k_init: int = 1, **k_means_args) -> None:  # noqa: ANN003
        """k_init : The initial number of clusters applied to KMeans()"""
        self.__k_init = k_init
        self.__k_means_args = k_means_args

    @staticmethod
    def calculate_cluster_amount(matrix_x: NDArray[np.float64]) -> int:
        """## クラスタ数を計算し、クラスタごとのサイズを返す"""
        matrix_x_standardized = stats.zscore(matrix_x)

        clusters = ConvergenceJudgment(random_state=1).fit(matrix_x_standardized).cluster_sizes_

        return len(clusters)

    def fit(self, matrix_x: NDArray[np.float64]) -> "ConvergenceJudgment":
        self.__clusters: list[Cluster] = []

        clusters = Cluster.build(
            matrix_x, KMeans(self.__k_init, **self.__k_means_args).fit(matrix_x)
        )
        self.__recursively_split(clusters)

        self.labels_ = np.empty(matrix_x.shape[0], dtype=np.intp)
        for i, c in enumerate(self.__clusters):
            self.labels_[c.index] = i

        self.cluster_centers_ = np.array([c.center for c in self.__clusters])
        self.cluster_log_likelihoods_ = np.array([c.log_likelihood() for c in self.__clusters])
        self.cluster_sizes_ = np.array([c.size for c in self.__clusters])

        return self

    def __recursively_split(self, clusters: list[Cluster]) -> None:
        for cluster in clusters:
            if cluster.size <= 3:  # noqa: PLR2004
                self.__clusters.append(cluster)
                continue

            k_means = KMeans(2, **self.__k_means_args).fit(cluster.data)
            c1, c2 = Cluster.build(cluster.data, k_means, cluster.index)

            beta = np.linalg.norm(c1.center - c2.center) / np.sqrt(
                np.linalg.det(c1.cov) + np.linalg.det(c2.cov)
            )
            alpha = 0.5 / stats.norm.cdf(beta)
            bic = -2 * (
                cluster.size * np.log(alpha) + c1.log_likelihood() + c2.log_likelihood()
            ) + 2 * cluster.df * np.log(cluster.size)

            if bic < cluster.bic():
                self.__recursively_split([c1, c2])
            else:
                self.__clusters.append(cluster)

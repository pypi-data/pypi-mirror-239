import numpy as np
import math
from sklearn.cluster import DBSCAN


class Outline:
    def __init__(self, data):
        self.data = data

    # среднее и отклонение
    def detect_outlier_mean_std(self, column_name, threshold=1.5):
        mean = self.data[column_name].mean()
        std = self.data[column_name].std()
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std

        outliers = (self.data[column_name] >= lower_bound) & (self.data[column_name] >= upper_bound)
        return self.data[outliers]

    # квартили
    def detect_outlier_kvart(self, column_name, threshold=1.5):
        # threshold определяет, насколько далеко за пределами межквартильного диапазона (IQR) считать точку выбросом. 1.5 - стандартное значение
        Q1 = self.data[column_name].quantile(0.25)
        Q3 = self.data[column_name].quantile(0.75)

        IQR = Q3 - Q1

        lower_threshold = Q1 - threshold * IQR
        upper_threshold = Q3 + threshold * IQR

        outliers = (self.data[column_name] < lower_threshold) | (self.data[column_name] > upper_threshold)

        return self.data[outliers]

    # Шовене
    def detect_outlier_shovene(self, column_name):
        ans = []

        n = self.data[column_name].count()
        mean = self.data[column_name].mean()
        std = self.data[column_name].std()

        for index, value in self.data.iterrows():
            if math.erfc((abs(value[column_name] - mean)) / std) < 1 / (2 * n):
                ans.append(index)
            else:
                n -= 1
        return ans

    # по двум переменным (подсказали про кластеризацию и dbscan на паре)
    def detect_outlier_dbscan(self, col1, col2, eps, min_samples):
        column_data = self.data[[col1, col2]].to_numpy()

        dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(column_data)
        labels = dbscan.labels_

        # Вычисление количества элементов в каждом кластере
        unique, counts = np.unique(labels, return_counts=True)
        clusters_counts = dict(zip(unique, counts))

        # Поиск кластеров с количеством элементов <= 2
        small_clusters = [cluster for cluster, count in clusters_counts.items() if count <= 2]

        # Возвращение индексов строк для этих кластеров
        outlier_indices = self.data.index[np.isin(labels, small_clusters)].tolist()

        return outlier_indices

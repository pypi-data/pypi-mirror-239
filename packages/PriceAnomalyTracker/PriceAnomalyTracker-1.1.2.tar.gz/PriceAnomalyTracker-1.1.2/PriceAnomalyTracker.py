import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from scipy.stats import shapiro

def PriceAnomalyTracker(data, threshold_shapiro=0.05, init_clusters=10, min_samples=2, min_lenght=5, sense=1):
    data = np.array(data).reshape(-1, 1)
    results = []
    if len(data) > 2:  # Garantindo ao menos 2 pontos para inicializar a detecção de anomalias

        statistic, p_value = shapiro(data) # Realizando o teste estatístico de Shapiro

        if p_value < threshold_shapiro: # Se o p_value de Shapiro demonstrar um comportamento não normal dos dados, iniciamos um método com DBSCAN

            # Iniciando um teste de variância dos clusters KMeans para determinar o número máximo ideal para o método
            previous_variance = float('inf')
            optimal_num_clusters = 1

            for n_clusters in range(1, init_clusters+1):
                kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=init_clusters)
                kmeans_model.fit(data)
                variance = kmeans_model.inertia_

                if n_clusters > 2 and variance <= previous_variance:
                    optimal_num_clusters = n_clusters - 1
                    break

                previous_variance = variance

            # Aplicando o KMeans após encontrar o número ótimo de clusters
            kmeans_model = KMeans(n_clusters=optimal_num_clusters, random_state=42, n_init=10)
            kmeans_model.fit(data)

            # Adquirindo a quantidades de clusters e seus respectivos centros
            cluster_centers = kmeans_model.cluster_centers_

            # Calculando as distâncias espaciais entre os centros dos clusters
            centroids_before_calculation = []
            for i, center in enumerate(cluster_centers):
                for j in range(i + 1, len(cluster_centers)):
                    spatial_distance = abs(center[0] - cluster_centers[j][0]) / optimal_num_clusters
                    centroids_before_calculation.append(spatial_distance)

            # Calculando a média das distâncias espaciais para atribuir ao eps que será usado no DBSCAN
            eps = np.mean(centroids_before_calculation)
            eps = eps*sense

            # Definindo o mínimo de amostras para determinar se os dados podem fazer parte de um mesmo cluster. Se refere à densidade.
            if len(data) > min_lenght: # Se o comprimento dos dados for maior que min_lenght, o min_samples será o inteiro mais próximo de min_lenght/2.
                min_samples = int(round(len(data) / 2, 0))
            else:
              min_samples = min_samples

            # Configurando o DBSCAN
            dbscan_model = DBSCAN(eps=eps, min_samples=min_samples)

            # Aplicando o DBSCAN configurado nos dados
            labels = dbscan_model.fit_predict(data)

            # Identificando anomalias e atribuindo status
            anomalies_dbscan = data[labels == -1]
            for value in data:
                if value in anomalies_dbscan:
                    results.append([value[0], True])
                else:
                    results.append([value[0], False])
        else: # Se o p_value de Shapiro demonstrar um comportamento normal dos dados, iniciamos um método com KMeans apenas

            num_clusters = 1

            # Aplicando o método KMeans
            kmeans_model = KMeans(n_clusters=num_clusters, random_state=42, n_init=init_clusters)
            kmeans_model.fit(data)

            # Adquirindo a quantidades de clusters e seus respectivos centros
            cluster_centers = kmeans_model.cluster_centers_

            # Definindo o Threshold: considerar o módulo do vetor de raio do cluster como a média/2 dos dados.
            anomaly_threshold = np.mean(data) / 2
            anomaly_threshold = anomaly_threshold*sense
            # Detectando pontos fora do raio como anomalias e atribuindo status
            anomalies_kmeans = data[(data < cluster_centers.min() - anomaly_threshold) | (data > cluster_centers.max() + anomaly_threshold)]
            for value in data:
                if value in anomalies_kmeans:
                    results.append([value[0], True])
                else:
                    results.append([value[0], False])
    else: # Caso contrário, não há valores anômalos
        for value in data:
            results.append([value[0], False])

    return results
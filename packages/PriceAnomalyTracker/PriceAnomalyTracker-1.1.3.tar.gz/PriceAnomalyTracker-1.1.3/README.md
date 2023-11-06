# PriceAnomalyTracker

PriceAnomalyTracker é uma biblioteca Python para detecção de anomalias em séries de dados. Utilizando métodos de aprendizado não supervisionado, ela aplica técnicas de clusterização (como K-Means e DBSCAN) e testes de normalidade (como o Teste de Shapiro) para identificar anomalias em uma ampla variedade de dados.

PriceAnomalyTracker pode ser aplicado em várias áreas, incluindo finanças, detecção de fraudes, monitoramento de sensores, análise de preços de produtos e muito mais.

PriceAnomalyTracker é especialmente útil quando você precisa detectar anomalias em dados de um mesmo grupo. Por exemplo, pode ser usado para identificar preços anômalos na venda de um modelo específico de carro, onde os preços devem estar próximos e seguir uma tendência semelhante. A biblioteca é versátil o suficiente para ser aplicada em várias situações em que você deseja encontrar discrepâncias em dados que compartilham características comuns.


## Instalação e Utilização

From PyPI:

```
pip install PriceAnomalyTracker
```

```
# Exemplo de uso para detectar anomalias em preços de um determinado produto

import PriceAnomalyTracker as PAT

data = [4250.2, 6665.5, 6665.6, 6665.56, 6135.12, 6665.6, 6672.2, 7221.1, 7221.1, 7799.0, 7852.9]

results = PAT.PriceAnomalyTracker(data)

for item in results:
    value, is_anomaly = item
    if is_anomaly:
        print(f"Anomalia detectada: {value}")
    else:
        print(f"Valor normal: {value}")
```

From GitHub:

```
!git clone https://github.com/RobertoJuniorXYZ/PriceAnomalyTracker.git
```

```
# Exemplo de uso para detectar anomalias em preços de um determinado produto

import sys
sys.path.append('PriceAnomalyTracker')

from PriceAnomalyTracker import PriceAnomalyTracker as PAT

data = [4250.2, 6665.5, 6665.6, 6665.56, 6135.12, 6665.6, 6672.2, 7221.1, 7221.1, 7799.0, 7852.9]

results = PAT.PriceAnomalyTracker(data)

for item in results:
    value, is_anomaly = item
    if is_anomaly:
        print(f"Anomalia detectada: {value}")
    else:
        print(f"Valor normal: {value}")
```

## Parâmetros
#### data (Obrigatório):
Uma lista contendo os valores a serem analisados.
#### threshold_shapiro (Opcional):
O valor de significância para o teste de normalidade de Shapiro (padrão é 0.05).
#### init_clusters (Opcional):
Número máximo de clusters a serem testados no método K-Means (padrão é 10).
#### min_samples (Opcional):
Número mínimo de amostras para formar um cluster no DBSCAN (padrão é 2).
#### min_lenght (Opcional):
Comprimento mínimo dos dados para definir min_samples como metade desse valor (padrão é 5).
#### sense (Opcional):
Um fator para ajustar o limiar de anomalia (padrão é 1).


## Contribuição
Se você encontrar algum problema ou quiser contribuir para melhorar o PriceAnomalyTracker, sinta-se à vontade para criar um problema no repositório ou enviar um pedido de pull.

## Licença
The MIT License (MIT)

Copyright (c) 2023 Roberto Junior

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
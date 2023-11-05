from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()
    
setup(name='PriceAnomalyTracker',
    version='1.0',
    license='MIT License',
    author='Roberto Junior',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='robertocarlosifrj@gmail.com',
    keywords='price anomaly tracker',
    description='PriceAnomalyTracker é uma biblioteca Python para detecção de anomalias em séries de dados. Utilizando métodos de aprendizado não supervisionado, ela aplica técnicas de clusterização (como K-Means e DBSCAN) e testes de normalidade (como o Teste de Shapiro) para identificar anomalias em uma ampla variedade de dados.',
    install_requires=['numpy', 'scikit-learn', 'scipy'])
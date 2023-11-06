from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()
    
setup(name='PriceAnomalyTracker',
    version='1.1.3',
    license='MIT License',
    author='Roberto Junior',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='robertocarlosifrj@gmail.com',
    keywords='price anomaly tracker',
    description='PriceAnomalyTracker is a Python library for detecting anomalies in time series data. Using unsupervised learning methods, it applies clustering techniques (such as K-Means and DBSCAN) and normality tests (such as the Shapiro Test) to identify anomalies in a wide range of data.',
    install_requires=['numpy', 'scikit-learn', 'scipy'],
    url='https://github.com/RobertoJuniorXYZ/PriceAnomalyTracker',
    project_urls={
        'Documentation': 'https://github.com/RobertoJuniorXYZ/PriceAnomalyTracker/wiki',
        'PyPI': 'https://pypi.org/project/PriceAnomalyTracker/',
        'Source': 'https://github.com/RobertoJuniorXYZ/PriceAnomalyTracker/',
    }
)
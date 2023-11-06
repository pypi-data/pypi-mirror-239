from setuptools import setup, find_packages

setup(
    name='math_quiz_Eid',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
        'pytest',
        'pytest-cov',
        'coverage',
        'flake8',
        'black',
        'sphinx',
        'sphinx_rtd_theme',
        'sphinx-click',
        'sphinxcontrib-napoleon',
        ],
)

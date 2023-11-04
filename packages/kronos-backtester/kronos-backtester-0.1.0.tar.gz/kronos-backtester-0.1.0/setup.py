from setuptools import setup, find_packages

setup(
    name='kronos-backtester',
    version='0.1.0',
    author='Quant Illinois',
    author_email='quant.illinois@gmail.com',
    description='A backtesting framework for the trading strategies developed by Quant Illinois.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
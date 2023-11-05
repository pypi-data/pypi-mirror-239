from setuptools import setup

setup(
    name = 'meu-pacote-mab',
    version='0.0.1',
    packages = ['meu_pacote'],
    install_requires = ['httpx'],
    entry_points = {
        'console_scripts': ['meu_cli = meu_pacote.minha_lib:cli']
    }
)
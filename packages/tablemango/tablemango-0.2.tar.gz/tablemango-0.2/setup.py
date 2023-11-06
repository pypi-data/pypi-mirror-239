from setuptools import setup, find_packages

setup(
    name='tablemango',
    version='0.2',
    description='Solve N-Queens or Tower of Hanoi and copy results to clipboard',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
    ],
)

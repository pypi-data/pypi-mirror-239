from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='jigi',
    version='1.0.0',
    description='JIGI',
    author='Baxromov Shahzodbek',
    author_email='baxromov.shahzodbek@gmail.com',
    url='https://github.com/baxromov/JIGI.git',
    packages=['jigi'],
    install_requires=required
)

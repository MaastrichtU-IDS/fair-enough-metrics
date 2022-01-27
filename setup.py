from setuptools import setup, find_packages

setup(
    name='FAIR Enough metrics tests servive',
    version='0.1.0',
    url='https://github.com/MaastrichtU-IDS/fair-enough-metrics.git',
    author='Vincent Emonet',
    author_email='vincent.emonet@gmail.com',
    description='FAIR Enough metrics tests service.',
    packages=find_packages(),
    install_requires=open("requirements.txt", "r").readlines(),
)
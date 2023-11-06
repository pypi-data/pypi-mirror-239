from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='xdl',  # required
    version='2023.11.5',
    description='xdl: Deep Learning with Xarray',
    long_description=long_description,
    author='Feng Zhu',
    author_email='fengzhu@ucar.edu',
    url='https://github.com/fzhu2e/xdl',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='deep learning, xarray',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'colorama',
        'tqdm',
        'seaborn',
        'netCDF4',
        'xarray',
        'lightning',
        'torchmetrics',
    ],
)

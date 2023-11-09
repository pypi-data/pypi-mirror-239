import sys
from setuptools import setup, find_packages

setup(
    name="earfcn",
    version='0.0.1',
    author='Alex Marder',
    # author_email='notlisted',
    description="Convert LTE EARFCN to frequency, or frequency to EARFCN.",
    url="https://gitlab.com/alexander_marder/earfcn",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'earfcn2freq=earfcn.convert:earfcn2freq_main',
            'freq2earfcn=earfcn.convert:freq2earfcn_main',
        ],
    },
    # install_requires=['numpy'],
    zip_safe=False,
    readme='README.md',
    include_package_data=True,
    python_requires='>3.6'
)

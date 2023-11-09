from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Leppa'
 
# Setting up
setup(
    name="leppa",
    version=VERSION,
    author="Hrushikesh Kachgunde",
    author_email="<hrushiskachgunde@gmail.com>",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'scikit-learn', 'qiskit', 'qiskit-ibmq-provider', 'pylatexenc', 'qiskit-ignis', 'qiskit-aer', 'genomic-benchmarks'],
    keywords=['python', 'neural networks', 'ann', 'prediction', 'ART neural network'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
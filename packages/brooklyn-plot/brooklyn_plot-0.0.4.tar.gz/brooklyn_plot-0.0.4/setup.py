from setuptools import setup, find_packages, find_namespace_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
        name='brooklyn_plot',
        version='0.0.4',
        author='Arun Patil, Matthew McCall and Marc Halushka',
        author_email='halushm@ccf.org',
        url='https://github.com/arunhpatil/brooklyn/',
        description='Gene co-expression and transcriptional bursting pattern recognition tool in single cell/nucleus RNA-sequencing data',
        long_description=long_description,
        keywords=['brooklyn', 'single cell', 'single nucleus', 'single cell-RNA', 'single nucleus-RNA', 'RNA analysis', 'cellxgene', 'RNA-seq', 'bioinformatics tools', 'co-expression', 'transcriptional bursting', 'sc-RNAseq', 'sn-RNAseq'],  # arbitrary keywords
        license='MIT',
        package_dir={'brooklyn_plot': 'brooklyn_plot'},
        packages=find_packages(),
        package_data = {'':['rScripts/*.R', 'libs/*.py']},
        install_requires=['scanpy','pandas','numpy','scipy','rpy2'],
        entry_points={'console_scripts': ['brooklyn_plot = brooklyn_plot.__main__:main']},
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Programming Language :: Python :: 3.8",
            "Topic :: Scientific/Engineering :: Bio-Informatics"
            ],
        include_package_data=True,
        python_requires='>=3.7',
)

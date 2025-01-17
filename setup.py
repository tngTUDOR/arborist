from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='arborist',
    version="0.3",
    packages=find_packages(),
    author="BONSAI team",
    author_email="info@bonsai.uno",
    license=open('LICENSE').read(),
    package_data={'arborist': package_files(os.path.join('arborist', 'data'))},
    entry_points = {
        'console_scripts': [
            'arborist-cli = arborist.bin.arborist_cli:main',
        ]
    },
    install_requires=[
        'docopt',
        'pandas',
        'rdflib',
        'xlrd',
    ],
    url="https://github.com/BONSAMURAIS/arborist",
    long_description=open('README.md').read(),
    description="Generate the URIs needed for the BONSAI knowledge graph",
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

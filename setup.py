from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

# Probably should be changed, __init__.py is no longer required for Python 3
for dirpath, dirnames, filenames in os.walk('arborist'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='arborist',
    version="0.1",
    packages=packages,
    author="BONSAI team",
    author_email="info@bonsai.uno",
    license=open('LICENSE').read(),
    # Only if you have non-python data (CSV, etc.). Might need to change the directory name as well.
    # package_data={'your_name_here': package_files(os.path.join('arborist', 'data'))},
    entry_points = {
        'console_scripts': [
            'arborist-cli = arborist.bin.rename_me_cli:main',
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

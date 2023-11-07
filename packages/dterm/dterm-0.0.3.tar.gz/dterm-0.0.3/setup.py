import os
import setuptools
from distutils.core import setup

REQUIRED = ['networkx']

BIN_DIR = os.path.dirname(os.path.realpath(__file__))

EXTRAS = {
    # 'datadog': ["datadog"],
}

setup(
    name='dterm',
    version='0.0.3',  # open("VERSION", "r").read(),
    packages=setuptools.find_packages(),  # ['dterm'],
    package_data={'': ['README.md']},
    description="Data Engineering Terminal Scripts",
    long_description="""Data Engineering terminal utilities.

- dbt exposure generation
- lineage impact reports

    """,
    # long_description=open('README2.0.md').read(),
    long_description_content_type="text/markdown",
    author='trevor grayson',
    author_email='trevor@dave.com',
    url='http://github.com/dave-inc/descript',

    scripts=['bin/dossier', 'bin/dterm'],
    # entry_points={ },

    # python_requires='3.11', #todo
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    # include_package_data=True,
    license='MIT',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 4',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        # 'Topic :: Software Development :: Libraries',
        # 'Topic :: System :: Monitoring',
        # 'Topic :: System :: Logging',
        # 'Programming Language :: Python :: 3.10',
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy'
    ],
    include_package_data=True
)

# https://github.com/kennethreitz/setup.py/blob/master/setup.py

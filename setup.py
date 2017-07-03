import setuptools

setuptools.setup(
    name='footballdata',
    version='0.2.0',
    url='https://github.com/skagr/footballdata',
    license='MIT',

    author='Skag Rijsdijk',
    author_email='skag.rijsdijk@gmail.com',

    description='A collection of wrappers over football (soccer) data '
                'from various websites / APIs. You get: Pandas dataframes '
                 'with sensible, matching column names and identifiers '
                 'across datasets. Data is downloaded when needed and cached '
                 'locally. Example Jupyter Notebooks are in the Github repo.',

    long_description=open('README.rst').read(),

    packages=['footballdata'],

    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'pathlib2;python_version<"3.4"'
    ],

    extras_require={
        'test': ['pytest'],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords=['football', 'soccer', 'metrics', 'sports', 'statistics'],
)

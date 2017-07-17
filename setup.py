import setuptools

setuptools.setup(
    name='footballdata',
    version='0.3.1',
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
        'unidecode',
        'pathlib2;python_version<"3.4"'
    ],

    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords=['football', 'soccer', 'metrics', 'sports', 'statistics'],
)

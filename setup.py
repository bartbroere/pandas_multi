from setuptools import setup

with open('README.md', 'r') as readme:
    readme = "".join(readme.readlines())

with open('requirements.in', 'r') as requirements:
    dependencies = [dependency.split('#')[0].replace('\n', '').replace(' ', '')
                    for dependency in requirements.readlines() if
                    dependency[0] != '#']

setup(
    name='pandas_multi',
    version='2018.7.30',
    url='https://github.com/bartbroere/pandas_multi/',
    author='Bart Broere',
    author_email='mail@bartbroere.eu',
    license='MIT License',
    description="Read multiple csvs as a single pandas DataFrame.",
    keywords='pandas readcsv readcsvs csv dataframe multiple multi',
    long_description=readme,
    py_modules=['pandas_multi'],
    install_requires=dependencies,
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    )
)

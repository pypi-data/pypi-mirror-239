from setuptools import setup, find_packages


classifiers=[
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3"
]


install_requires=[
    "yxdb>=1.0.0",
    "pandas>=2.0.3"
]


setup(
    name='import_yxdb',
    version='1.0.0',
    author='Mikkel Thorhauge',
    author_email='',
    url='',
    license='MIT',
    classifiers=classifiers,
    description='Import yxdb into a dictionary or a Pandas dataframe',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    keywords=['Alteryx','yxdb', 'Pandas dataframe', 'import'],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.8.18'
)
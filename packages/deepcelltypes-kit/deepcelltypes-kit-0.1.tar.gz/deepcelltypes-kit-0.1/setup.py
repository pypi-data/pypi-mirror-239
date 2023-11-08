from setuptools import setup, find_packages

setup(
    name='deepcelltypes-kit',
    version='0.1',
    packages=find_packages(),
    description='A library for the deepcelltypes project.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='xuefei-wang',
    author_email='wang.xuefei.wang@gmail.com',
    url='https://github.com/xuefei-wang/deepcelltypes-kit',
    install_requires=[
        'numpy', 

    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

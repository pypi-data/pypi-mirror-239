from setuptools import setup

setup(
    name='rcquant_sdk',
    version='0.0.1',
    description='rcquant_sdk',
    author='rcquant_sdk',
    author_email='rcquant_sdk@example.com',
    packages=['rcquant_sdk'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'msgpack',
        'numpy',
        'pandas',
    ],
    python_requires='>=3.6',
)
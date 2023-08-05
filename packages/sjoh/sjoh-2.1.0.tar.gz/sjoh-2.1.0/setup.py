
from setuptools import setup

setup(
    name='sjoh',
    version='2.1.0',
    url='https://github.com/nicolas-van/sjoh.py',
    license='MIT',
    author='Nicolas Vanhoren',
    author_email='nicolas.vanhoren@gmail.com',
    description='Implementation of the Simple JSON over HTTP protocol.',
    long_description=__doc__,
    packages=[
        'sjoh'
    ],
    install_requires=[
        'requests>=2.2.1',
    ],
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)


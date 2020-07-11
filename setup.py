"""A setuptools based setup module."""
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(
    name='qencode',
    version='1.0',
    description="Python bindings for the Qencode API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qencode-dev/qencode-api-python-client',
    author='Qencode Developer',
    author_email='team@qencode.com',
    license='proprietary',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='qencode, qencode.com, cloud.qencode.com',
    packages=['qencode'],
)

"""A setuptools based setup module.
"""

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open('LONG_DESCRIPTION.md') as f:
    long_description = f.read()

setup(
    name='qencode',
    version='0.9.27',
    description="Client library for main features and functionality of Qencode for Python v2.x.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qencode-dev/qencode-api-python-client',
    # url=here,
    author='Qencode Developer',
    author_email='team@qencode.com',
    license='proprietary',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2.7'

    ],
    keywords='qencode, qencode.com, cloud.qencode.com',
    packages=['qencode']
)

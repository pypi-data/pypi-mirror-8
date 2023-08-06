#!/usr/bin/env python

from distutils.core import setup

setup(
    name='kryptonite',
    packages=['kryptonite'],
    license='MIT',
    version='0.1.3',
    description='Cryptography for humans',
    long_description='',
    author='Gil Shotan',
    author_email='gil@gilshotan.com',
    url='https://github.com/gilsho/kryptonite',
    download_url='https://github.com/gilsho/kryptonite/tarball/0.1.3',
    keywords='cryptography security encryption decryption',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],
    install_requires=['pycrypto', 'passlib']
)

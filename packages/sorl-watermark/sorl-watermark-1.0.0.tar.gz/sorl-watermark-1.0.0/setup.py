from setuptools import setup
from setuptools import find_packages

setup(
    name='sorl-watermark',
    version='1.0.0',
    url='https://github.com/originell/sorl-watermark',
    author='Luis Nell',
    author_email='cooperate@originell.org',
    packages=find_packages(),
    platforms='any',
    description='Image based watermarks for sorl-thumbnail',
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics"
    ],
    install_requires=[
        'sorl-thumbnail',
    ],
)

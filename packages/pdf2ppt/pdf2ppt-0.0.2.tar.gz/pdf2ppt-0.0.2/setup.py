# setup.py
from setuptools import setup, find_packages
from pdf2ppt.version import __version__


setup(
    name='pdf2ppt',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'python-pptx',
        'pdf2image',
        'pqdm',
    ],
    entry_points={
        'console_scripts': [
            'pdf2ppt=pdf2ppt.pdf2ppt:main',
        ],
    },
    author='Zihao Fu',
    description='A tool to convert PDF documents to PPTX format with an adjustable DPI setting.',
    keywords='PDF PPTX conversion tool',
    url='https://github.com/fuzihaofzh/pdf2ppt',  # Replace with the actual URL
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Office Suites',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

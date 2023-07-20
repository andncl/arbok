from setuptools import setup, find_packages

setup(
    name='arbok',
    version='0.1',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'qcodes',
        'qm-qua',
        'qualang-tools'
        'quantify-core'
        # List your dependencies here
    ],
)

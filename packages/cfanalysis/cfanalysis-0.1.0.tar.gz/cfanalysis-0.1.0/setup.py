from setuptools import find_packages, setup

setup(
    name='cfanalysis',
    packages=find_packages(include=['cfanalysis']),
    version='0.1.0',
    description='Library to perform Combinatorial Fusion Analysis',
    author='Mohammed Quazi',
    author_email='ashasquazi@gmail.com',
    install_requires=['numpy', 'pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='test',
)
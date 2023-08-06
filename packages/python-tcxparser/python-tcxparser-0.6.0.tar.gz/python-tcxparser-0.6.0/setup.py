from setuptools import setup

__version__ = '0.6.0'

setup(
    name='python-tcxparser',
    version=__version__,
    author='Vinod Kurup',
    author_email='vinod@kurup.com',
    py_modules=['tcxparser', 'test_tcxparser'],
    url='https://github.com/vkurup/python-tcxparser/',
    license='BSD',
    description='Simple parser for Garmin TCX files',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description=open('README.md').read(),
    install_requires=[
        "lxml",
    ],
    test_suite="test_tcxparser",
)

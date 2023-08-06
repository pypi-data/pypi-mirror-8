try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = ['requests>=2.1.0']

setup(
    name='fulcrum',
    version='1.3.0',
    description='A python wrapper for the Fulcrum API',
    author='Jason Sanford',
    author_email='jasonsanford@gmail.com',
    url='https://github.com/fulcrumapp/fulcrum-python',
    packages= ['fulcrum', 'fulcrum.api'],
    install_requires=requires,
    license='Apache License',
)

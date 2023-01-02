from setuptools import setup

# This setup.py file is based on:
# https://uoftcoders.github.io/studyGroup/lessons/python/packages/lesson/
setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='PySeshat',
    url='https://github.com/MichaelHoltonPrice/pyseshat',
    author='Michael Holton Price',
    author_email='MichaelHoltonPrice@gmail.com',
    # Needed to actually package something
    packages=['pyseshat'],
    # Needed for dependencies
    install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT', # TODO: will this do?
    description='A Python package for working with the Seshat Global History\
        Databank',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
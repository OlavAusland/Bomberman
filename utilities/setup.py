from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='utilities',
    url='https://github.com/CarelessDeveloper/utilities.git',
    author='Olav Onstad',
    author_email='CarelessDeveloper@hotmail.com',
    # Needed to actually package something
    packages=['utilities'],
    # Needed for dependencies
    install_requires=['os'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='A package which helps you to style you cmd window easier',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
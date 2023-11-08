from setuptools import setup

# Read the contents of requirements.txt
with open('requirement.txt', 'r') as file:
    requirements = file.read().splitlines()

setup(
    name='',
    version='0.0.1',
    author='Manish Uniyal',
    author_email='uniyalmanish578@gmail.com',
    description='Python module to onboard the TR broker platform',
    packages=['trBroker'],
    install_requires=requirements,
)
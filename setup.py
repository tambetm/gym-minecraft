from setuptools import setup, find_packages
import sys, os

# Don't import gym module here, since deps may not be installed
for package in find_packages():
    if '_gym_' in package:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), package))
from package_info import USERNAME, VERSION

setup(name='{}_{}'.format(USERNAME, 'gym_minecraft'),
    version=VERSION,
    description='Gym User Env - 15 Minecraft scenarios based on Malmo',
    url='https://github.com/tambetm/gym_minecraft',
    author='Tambet Matiisen',
    author_email='tambet.matiisen@gmail.com',
    license='MIT License',
    packages=[package for package in find_packages() if package.startswith(USERNAME)],
    package_data={ '{}_{}'.format(USERNAME, 'gym_minecraft'): ['assets/*.xml' ] },
    zip_safe=False,
    install_requires=[ 'gym>=0.2.3' ],
)

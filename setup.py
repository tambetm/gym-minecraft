from setuptools import setup, find_packages

setup(name='gym_minecraft',
      version='0.0.2',
      description='OpenAI Gym environment for Minecraft based on Malmo',
      url='https://github.com/tambetm/gym-minecraft',
      author='Tambet Matiisen',
      author_email='tambet.matiisen@gmail.com',
      license='MIT License',
      packages=find_packages(),
      package_data={'': ['assets/*.xml']},
      zip_safe=False,
      install_requires=['gym>=0.2.3'],
      dependency_links=['git+https://github.com/tambetm/minecraft-py.git']
)

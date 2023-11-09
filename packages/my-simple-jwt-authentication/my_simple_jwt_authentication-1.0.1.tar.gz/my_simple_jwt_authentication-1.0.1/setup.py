from setuptools import setup


# specify requirements of your package here
REQUIREMENTS = ['pyjwt', 'pytz']

# some more details
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    ]

# calling the setup function 
setup(name='my_simple_jwt_authentication',
      version='1.0.1',
      description='A simple jwt authenticaion module.',
      author='Mahdi Abrishami',
      author_email='mabrishami00@gmail.com',
      license='MIT',
      packages=['my_simple_jwt_auth'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='jwt authentication'
      )

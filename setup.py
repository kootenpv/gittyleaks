from setuptools import setup

MAJOR_VERSION = '0'
MINOR_VERSION = '0'
MICRO_VERSION = '11'
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(name = 'gittyleaks',
      version = VERSION,
      description = 'Discover where your sensitive data has been leaked.',
      url = 'https://github.com/kootenpv/gittyleaks',
      author = 'Pascal van Kooten',
      author_email = 'kootenpv@gmail.com',
      license = 'GPL',
      packages = ['gittyleaks'],
      install_requires = [ 
          'scandir',
      ], 
      entry_points = { 
          'console_scripts': ['gittyleaks = gittyleaks.gittyleaks:main'] 
      },
      zip_safe = False)

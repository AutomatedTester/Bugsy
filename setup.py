from setuptools import setup, find_packages

setup(name='bugsy',
      version='0.4.1',
      description='A library for interacting Bugzilla Native REST API',
      author='David Burns',
      author_email='david.burns at theautomatedtester dot co dot uk',
      url='http://oss.theautomatedtester.co.uk/bugzilla',
      classifiers=['Development Status :: 3 - Alpha',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: Apache Software License',
                  'Operating System :: POSIX',
                  'Operating System :: Microsoft :: Windows',
                  'Operating System :: MacOS :: MacOS X',
                  'Topic :: Software Development :: Libraries',
                  'Programming Language :: Python'],
        packages = find_packages(),
        install_requires=['requests>=1.1.0'],
        )

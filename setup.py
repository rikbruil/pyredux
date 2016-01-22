import unittest
import sys
from setuptools import setup, Command


class RunTests(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        loader = unittest.TestLoader()
        tests = loader.discover('tests', pattern='*_test.py', top_level_dir='.')
        runner = unittest.TextTestRunner()
        results = runner.run(tests)
        sys.exit(0 if results.wasSuccessful() else 1)


setup(name='pyredux',
      version='0.1',
      description='Port of the Redux library for Python and for fun',
      url='http://github.com/rikbruil/pyredux',
      author='Rik Bruil',
      author_email='rik.bruil@gmail.com',
      license='MIT',
      packages=['pyredux'],
      install_requires=[
          # 'markdown',
      ],
      zip_safe=False,
      cmdclass={'test': RunTests,},)

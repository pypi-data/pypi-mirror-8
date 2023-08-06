from setuptools import setup


setup(name='microasync',
      version='0.3',
      description='Green threads and CSP for micropython.',
      long_description=open('README.rst').read(),
      url='https://github.com/nvbn/microasync/',
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      license='MIT',
      packages=['microasync'])
#from microasync.async import do_all

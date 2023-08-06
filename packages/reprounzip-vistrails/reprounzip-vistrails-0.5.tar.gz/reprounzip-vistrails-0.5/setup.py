import os
from setuptools import setup
import sys


# pip workaround
os.chdir(os.path.abspath(os.path.dirname(__file__)))


with open('README.rst') as fp:
    description = fp.read()
req = [
    'reprounzip>=0.5',
    'rpaths>=0.8']
if sys.version_info < (2, 7):
    req.append('argparse')
setup(name='reprounzip-vistrails',
      version='0.5',
      packages=['reprounzip', 'reprounzip.plugins'],
      entry_points={
          'reprounzip.plugins': [
              'vistrails = reprounzip.plugins.vistrails:setup_vistrails']},
      namespace_packages=['reprounzip', 'reprounzip.plugins'],
      install_requires=req,
      description="Allows the ReproZip unpacker to create virtual machines",
      author="Remi Rampin, Fernando Chirigati, Dennis Shasha, Juliana Freire",
      author_email='reprozip-users@vgc.poly.edu',
      maintainer="Remi Rampin",
      maintainer_email='remirampin@gmail.com',
      url='http://vida-nyu.github.io/reprozip/',
      long_description=description,
      license='BSD',
      keywords=['reprozip', 'reprounzip', 'reproducibility', 'provenance',
                'vida', 'nyu', 'vistrails'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Topic :: Scientific/Engineering',
          'Topic :: System :: Archiving'])

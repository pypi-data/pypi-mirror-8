from setuptools import setup, find_packages
import os

version = '2.0dev3'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
TODO = open(os.path.join(here, 'TODO.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

install_requires = [
    'pyramid>=1.1a3',
    'geojson>=1.0',
    'Shapely>=1.2',
    'GeoAlchemy2>=0.2.4'
    ]

setup(name='papyrus',
      version=version,
      description="Geospatial Extensions for Pyramid",
      classifiers=[
          'Framework :: Pyramid',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP',
      ],
      keywords='FOSS4G, Pylons, Pyramid',
      author='Eric Lemoine',
      author_email='eric.lemoine@gmail.com',
      url='https://github.com/elemoine/papyrus',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      long_description=README + '\n\n' + TODO + '\n\n' + CHANGES,
      )

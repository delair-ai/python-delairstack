"""Configure packaging.

"""

import re

from setuptools import setup, find_packages

with open('delairstack/__init__.py') as fh:
    for line in fh:
        m = re.match('^__version__\\s*=\\s*\'([0-9a-z.+-]+)\'', line)
        if m:
            VERSION = m.group(1)
            break
    else:
        raise RuntimeError('The __init__.py module must provide a version')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='python-delairstack',
      version=VERSION,
      license='MIT',
      description='High-level Python interface to Delair.ai API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Delair.ai Backend Team',
      author_email='backend-team@delair.aero',
      url='https://github.com/delair-ai/python-delairstack',
      install_requires=['urllib3>=1.23', 'requests-futures>=0.9.7', 'appdirs>=1.4.3', 'pathvalidate==0.29.1'],
      packages=find_packages(exclude=['docs', 'tests*', 'notebooks']),
      package_dir={'delairstack': 'delairstack'},
      package_data={
          'delairstack': ['logging.conf',
                          'core/utils/vertcrs/*.wkt']
          },
      test_suite='tests',
      tests_require=['urllib3-mock>=0.3.3'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='sdk delair delair.ai',
      extras_require={
          'development': ['pycodestyle>=2.4.0'],
          'coverage': ['coverage>=4.4'],
          'documentation': ['sphinx>=1.8.5', 'sphinx_rtd_theme',
                            'sphinx_autodoc_typehints',
                            'sphinx-autobuild', 'recommonmark']
          }
)

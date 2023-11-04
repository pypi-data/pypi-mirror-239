from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'pyvectorguidance',
  packages=find_packages(),
  license='Apache Software License',
  description = 'Vector Guidance methods implemented in Python.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Iftach Naftaly',
  author_email = 'iftahnaf@gmail.com',
  url = 'https://github.com/iftahnaf/pyvectorguidance',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['Python', 'Vector Guidance'],
  install_requires=[
          'numpy==1.26.0',
          'rich==13.3.1',
          'scipy==1.10.0'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.10'
  ],
)
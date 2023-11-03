from setuptools import find_packages, setup

# reading long description from file
with open('README.md') as file:
    long_description = file.read()

# specify requirements of your package here
REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.10',
    ]

# calling the setup function
setup(name='nirmal-bundle-test',
      version='1.0.1',
      description='Package bundling',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='',
      author='co.dx',
      author_email='co.dx@test.com',
      license='MIT',
      packages= find_packages(where = 'library-name'),
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='maps location address'
      )

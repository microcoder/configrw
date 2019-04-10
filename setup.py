from setuptools import setup, find_packages
import configrw


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='configrw',
    version=configrw.__version__,
    description='ConfigRW is a simple reader and writer config files based on key-value or INI-structure.',
    # The long_description is used in pypi.org as the README description of your package
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='microcoder',
    # author_email='vademenev@gmail.com',
    url='https://github.com/microcoder/configrw',
    packages=find_packages(),  # packages=['configrw'],  # same as name
    # install_requires=['bar', 'greek'],  # external packages as dependencies
)

# 1. Make pypi-package:
#       python setup.py sdist
# 2. Upload package in test repository:
#       python -m twine upload -r testpypi dist/configrw-1.0.0.tar.gz
# 3. Upload package in real repository:
#       python -m twine upload -r pypi dist/configrw-1.0.0.tar.gz

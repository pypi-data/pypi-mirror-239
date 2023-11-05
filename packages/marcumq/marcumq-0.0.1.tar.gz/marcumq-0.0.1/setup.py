# python setup.py sdist
# twine upload --repository pypitest dist/*
# twine upload dist/*

import os
import setuptools

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'marcumq', '__version__.py'), 'r') as _:
    exec(_.read(), about)

with open ('requirements.txt', 'r') as _:
    requires = [line.split()[0] for line in _]

setuptools.setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description='See: '+about['__url__'],
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False
)

!/bin/bash

python setup.py clean

python setup.py sdist bdist_wheel

# check package
twine check dist/*
twine upload dist/*

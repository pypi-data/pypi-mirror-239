# python-utils
mak.gnuoy's python utilities package

## pre-requisites
   ```
   $ pip install build --upgrade 
   $ pip install twine --upgrade 
   ```
   
## unit test
   ```
   $ export PYTHONPATH=$PYTHONPATH:./src
   $ python -m unittest -v tests.config
   ```

## build
   ```
   $ python -m build
   ```

## distribution 
  - test.pypi.org
   ```
   $ python -m twine upload -r testpypi dist/*
   ```
  - pypi.org
   ```
   $ python -m twine upload dist/*
   ```

## installation
  - test.pypi.org
   ```
   $ python -m pip install -i https://test.pypi.org/simple/ mak.gnuoy-python-utils
   ```
  - pypi.org
   ```
   $ python -m pip install mak.gnuoy-python-utils
   ```


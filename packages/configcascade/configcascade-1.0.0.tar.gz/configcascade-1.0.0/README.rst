configcascade
=============

.. image:: https://travis-ci.org/felixcarmona/configcascade.png?branch=master
    :target: https://travis-ci.org/felixcarmona/configcascade

.. image:: https://coveralls.io/repos/felixcarmona/configcascade/badge.png?branch=master
    :target: https://coveralls.io/r/felixcarmona/configcascade?branch=master

.. image:: https://pypip.in/d/configcascade/badge.png
    :target: https://pypi.python.org/pypi/configcascade/
    :alt: Downloads

.. image:: https://pypip.in/v/configcascade/badge.png
    :target: https://pypi.python.org/pypi/configcascade/
    :alt: Latest Version


A simple Configuration System which allows you to import and override or merge configuration parameters

Example
-------

.. code-block:: python
  from configcascade import Settings, YamlFileLoader
  
  
  file_loader = YamlFileLoader()
  settings = Settings(file_loader, ['foo'])  # the second parameter are a the settings you which you want to merge instead of override when you import
  result = settings.compile("file_a.yml")

**file_a.yml:**

.. code-block:: yaml

  imports:
    - file_b.yml
    - file_c.yml
  
  foo:
    - x
    - y
    - z
  
  test:
    - a
    

**file_b.yml:**

.. code-block:: yaml

  foo:
    - 5
    - 7
  
  bbbb: 8

**file_c.yml:**

.. code-block:: yaml
  
  test:
    - b

**The generated result will be:**

.. code-block:: yaml

  foo:
    - x
    - y
    - z
    - 5
    - 7
  
  bbbb: 8
  
  test:
    - a

pertinosdk
==========

Welcome to Pertino Python SDK


Example Usage
-------------

.. code-block:: python


  '''
  Created on Jul 26, 2014
  
  @author: lwoydziak
  '''
  from pertinosdk import PertinoSdk, where
  from jsonconfigfile import Env
          
  def test_whenOrgsAvailableThenCanListThem():
      pertinoSdk = PertinoSdk(Env().get("Pertino", "login"), Env().get("Pertino", "password"))
      organizations = pertinoSdk.listOrgs()
      assert len(organizations) > 0
      
  def test_whenDevicesInOrganizationsThenCanListThem():
      pertinoSdk = PertinoSdk(Env().get("Pertino", "login"), Env().get("Pertino", "password"))
      organizations = pertinoSdk.listOrgs()
      devices = pertinoSdk.listDevicesIn(organizations[0])
      assert len(devices) > 0
       
  def test_deleteMachinesWithNameContainingAuto():
      pertinoSdk = PertinoSdk(Env().get("Pertino", "login"), Env().get("Pertino", "password"))
      organizations = pertinoSdk.listOrgs()
      devices = pertinoSdk.listDevicesIn(organizations[0], where("hostName").contains("auto"))
      pertinoSdk.deleteFrom(organizations[0], devices)
      assert not pertinoSdk.listDevicesIn(organizations[0], where("hostName").contains("auto"))
      
To Build
--------

.. code-block:: python

  ant env
  ant init
  ant package

To run unit tests
--------------------------

.. code-block:: python

  ant test

To run acceptance tests
--------------------------------

Create a file with your Pertino credentials (see acceptance/conftest.py for format/name)

.. code-block:: python

  ant acceptance
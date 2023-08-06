restart_docker
===============

A tool for restarting docker containers if their configuration or base image changes.

Installation
-------------

.. code:: bash

    $ pip install docker-py

Configuration
--------------

.. code:: json

    {
        "image_name": "username/image",
        "container_name": "container",
        "environment": {
            "VAR1": "value1",
            "VAR2": 2
        },
        "ports": {
            "5000": "127.0.0.1:5000"
        }
    }

+----------------+----------+----------------------------------------------------------+
| Field          | Required | Description                                              |
+================+==========+==========================================================+
| image_name     | Yes      | Name of the docker image to base container on            |
+----------------+----------+----------------------------------------------------------+
| container_name | Yes      | Name of the docker container to create or update         |
+----------------+----------+----------------------------------------------------------+
| environment    | No       | Dictionary of key value pairs for the docker environment |
+----------------+----------+----------------------------------------------------------+
| ports          | No       | Dictionary of key value pairs for port mappings          |
+----------------+----------+----------------------------------------------------------+

Running
--------

.. code:: bash

    $ restart_docker <filename> <image version>

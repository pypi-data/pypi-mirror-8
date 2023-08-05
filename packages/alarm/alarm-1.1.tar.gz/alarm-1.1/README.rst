.. image:: https://badge.fury.io/py/alarm.png
    :target: http://badge.fury.io/py/alarm
.. image:: https://pypip.in/d/alarm/badge.png
    :target: https://pypi.python.org/pypi/alarm
.. image:: https://pypip.in/license/alarm/badge.png
    :target: https://pypi.python.org/pypi/alarm


CLI Alarm Clock
===============

Alarm is CLI utility written in Python language.

Requirements
------------

.. code-block:: bash

    - Python 2 or 3
    - Mplayer


Installation
------------

Using `pip <https://pip.pypa.io/en/latest/>`_ :

.. code-block:: bash

    $ pip install slpkg

    uninstall:

    $ pip uninstall slpkg
   

Command Line Tool Usage
-----------------------

.. code-block:: bash

    usage: alarm [-h] [-v]
                 [-s] <time> <song>

    optional arguments
      -h, --help       show this help message and exit
      -v, --version    print version and exit
      -s, --set        set time and sound
    
    example: alarm -s 06:00:00 /path/to/song.mp3


Example:

.. code-block:: bash
    
    $ alarm -s 05:40:12 /home/dslackw/Music/xristina.ogg

    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : 05:49:12                                                      |
    | Sound file in : /home/dslackw/Music/xristina.ogg                             |
    | Time : 05:17:40                                                              |
    +==============================================================================+

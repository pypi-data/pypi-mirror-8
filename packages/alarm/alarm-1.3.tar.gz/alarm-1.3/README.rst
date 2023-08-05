.. image:: https://badge.fury.io/py/alarm.png
    :target: http://badge.fury.io/py/alarm
.. image:: https://pypip.in/d/alarm/badge.png
    :target: https://pypi.python.org/pypi/alarm
.. image:: https://pypip.in/license/alarm/badge.png
    :target: https://pypi.python.org/pypi/alarm


.. contents:: Table of Contents:

CLI Alarm Clock
===============

Alarm is CLI utility written in Python language.

How works
---------

When the date and time coincides with the current the alarm starts 
playing the sound is selected for five consecutive times. You can 
pause the alarm by pressing 'p' or 'space' is an attempt to cancel the 
'q' or 'ESC'. Change the volume of the alarm by pressing '*' or '/'.

You can create a list and use it as an alarm sound:

.. code-block:: bash
    
    $ cat * .mp3> playlist.m3u
    $ alarm -s 17 07:05 ~/Music/playlist.m3u

You will find some sounds in folder alarm/sounds.
Some will make you laugh, have fun !!!
    
Requirements
------------

.. code-block:: bash

    - Python 2 or 3
    - Mplayer

Installation
------------

Using `pip <https://pip.pypa.io/en/latest/>`_ :

.. code-block:: bash

    $ pip install alarm

    uninstall:

    $ pip uninstall alarm
   

Command Line Tool Usage
-----------------------

.. code-block:: bash

    usage: alarm [-h] [-v]
                 [-s] <day> <alarm time> <song>

    optional arguments
      -h, --help       show this help message and exit
      -v, --version    print version and exit
      -s, --set        set alarm day, time and sound
    
    example: alarm -s 21 06:00 /path/to/song.mp3

Example:

.. code-block:: bash
   
    $ alarm -s 18 22:05 ~/alarm/sounds/wake_up.mp3

    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 22:05                                               |
    | Sound file : ~/alarm/sounds/wake_up.mp3                                      |
    | Time : 21:06:41                                                              |
    +==============================================================================+
    Press 'Ctrl + c' to cancel alarm ...


    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 22:05                                               |
    | Sound file :  ~/alarm/sounds/wake_up.mp3                                     |
    | Time : 22:05 Wake Up !                                                       |
    +==============================================================================+
    Press 'Ctrl + c' to cancel alarm ...
    __        __    _          _   _         _ 
    \ \      / /_ _| | _____  | | | |_ __   | |
     \ \ /\ / / _` | |/ / _ \ | | | | '_ \  | |
      \ V  V / (_| |   <  __/ | |_| | |_) | |_|
       \_/\_/ \__,_|_|\_\___|  \___/| .__/  (_)
                                    |_|
    
    Attempt 1

    MPlayer 1.1-4.8.2 (C) 2000-2012 MPlayer Team

    Playing /home/dslackw/alarm/sounds/wake_up.mp3.
    libavformat version 54.6.100 (internal)
    Audio only file format detected.
    Load subtitles in /home/dslackw/alarm/sounds/
    ==========================================================================
    Opening audio decoder: [mpg123] MPEG 1.0/2.0/2.5 layers I, II, III
    AUDIO: 44100 Hz, 2 ch, s16le, 128.0 kbit/9.07% (ratio: 16000->176400)
    Selected audio codec: [mpg123] afm: mpg123 (MPEG 1.0/2.0/2.5 layers I, II, III)
    ==========================================================================
    [AO OSS] audio_setup: Can't open audio device /dev/dsp: No such file or directory
    AO: [alsa] 48000Hz 2ch s16le (2 bytes per sample)
    Video: no video
    
    A:   0.9 (00.9) of 17.0 (17.0)  1.3%

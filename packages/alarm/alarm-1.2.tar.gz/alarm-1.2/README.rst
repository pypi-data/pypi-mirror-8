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
    
    example: alarm -s 17 06:00 /path/to/song.mp3


Example:

.. code-block:: bash
   
    $ alarm -s 17 22:05 ~/Music/xristina.ogg

    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 22:05                                               |
    | Sound file : /home/dslackw/Music/xristina.ogg                                |
    | Time : 21:06:41                                                              |
    +==============================================================================+



    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 22:05                                               |
    | Sound file : /home/dslackw/Music/xristina.ogg                                |
    | Time : 22:05 Wake Up !                                                       |
    +==============================================================================+
    __        __    _          _   _         _ 
    \ \      / /_ _| | _____  | | | |_ __   | |
     \ \ /\ / / _` | |/ / _ \ | | | | '_ \  | |
      \ V  V / (_| |   <  __/ | |_| | |_) | |_|
       \_/\_/ \__,_|_|\_\___|  \___/| .__/  (_)
                                    |_|

    MPlayer 1.1-4.8.2 (C) 2000-2012 MPlayer Team
    Playing /home/dslackw/Music/xristina.ogg.
    libavformat version 54.6.100 (internal)
    libavformat file format detected.
    [lavf] stream 0: audio (vorbis), -aid 0, -alang eng
    Load subtitles in /home/dslackw/Music/
    ==========================================================================
    Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders
    libavcodec version 54.23.100 (internal)
    AUDIO: 44100 Hz, 2 ch, s16le, 0.0 kbit/0.00% (ratio: 0->176400)
    Selected audio codec: [ffvorbis] afm: ffmpeg (FFmpeg Vorbis)
    ==========================================================================
    [AO OSS] audio_setup: Can't open audio device /dev/dsp: No such file or directory
    AO: [alsa] 48000Hz 2ch s16le (2 bytes per sample)
    Video: no video
    Starting playback...
    A: 205.9 (03:25.8) of 230.9 (03:50.9)  1.6%

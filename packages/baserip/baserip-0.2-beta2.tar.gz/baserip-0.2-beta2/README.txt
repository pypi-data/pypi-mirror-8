Baserip
=======

Baserip is a tool for copying a single video title from a DVD whilst 
transcoding it. The purpose of this is to make the video available 
to devices you may have which do not have a DVD player.

Baserip is designed to work with a clean DVD source like the ones you get 
on bought DVD disks.
Baserip was created because Acidrip is no longer being maintained 
and I found myself needing a DVD ripper, if you're interested a little more 
please see :ref:`motivation`. 

The design of Baserip was heavily influenced by Acidrip but has now 
significantly changed.
Baserip is, in fact, a simple front-end to avlib/avconv which is 
itself a front-end to some video encoding and decoding libraries. Everything 
that Baserip does can be achieved from the command line, Baserip just 
simplifies the process.


Installation
------------

Unpack the tarball and go into the top level directory. As root 
type::

    python3 setup.py install

The installation directory is usually:
/usr/local/lib/python3.x/dist-utils

Here you will find Baserip. Within Baserip you will find a "share" 
directory. In this there is a .desktop file and an icon. You can use 
these to manually add an entry to your desktop menu system.


Requirements
------------

In order to run Baserip you will need the following:

* Python3
* PyQt4
* pyudev
* avconv
* lsdvd
* mplayer2

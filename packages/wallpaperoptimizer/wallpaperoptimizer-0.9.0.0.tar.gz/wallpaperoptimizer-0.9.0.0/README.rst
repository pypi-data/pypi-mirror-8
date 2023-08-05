
===================
Wallpaper optimizer
===================
---------------------------------------------------------
Wallpaperoptimizer is wallpaper changer for multi screen.
---------------------------------------------------------

:Author:
  Katsuhiro Ogikubo
  oggyist@gmail.com

:Version:
  0.9.0.0

1.Introduction
==============
  wallpaper optimizer is a program that best to deploy the wallpaper in a multi-monitor use below.
  The features and mode of operation of the following, it works on Linux.

Operating environment
---------------------
  * I try at the desktop of the following

    - GNOME2
    - Unity (GNOME3)
    - GNOME shell (GNOME3)
    - Xfce4
    - LXDE
    
  * I try in the following distributions

    - CentOS 6.3
    - Ubuntu12.04 LTS
    - Ubuntu12.10
    - Ubuntu13.04
    - Linux mint 14
    - Linux mint 17
    - Xubuntu (Ubuntu12.10)
    - Lubuntu (Ubuntu12.10)
    - Ubuntu GNOME shell Remix 12.10

Operation mode
--------------
  * By specifying the various parameters from console to create and set wallpapers
  * In console below, change the wallpaper at a specified time every
  * As a GNOME applet to be placed in the GNOME panel behavior (GNOME2)
  * operation of the application as an indicator (GNOME3, Xfce4, LXDE)

Features
--------
  * Specify two image, you can perform optimal placement of image size and monitor size
  * The left and right separately for each monitor can arrange the images to the monitor, I can be specified on the written-down approach and the like (left and right)
  * (For example placement partitioning of widgets) that you can specify the margin from the monitor end
  * You can change from the panel on the On / Off changer (only GNOME2)
  * Wallpaper setting can work with one specification image 1
  
  In addition, the following functions are not be implemented.
  * The rotation of the monitor, if you are using a vertical
  * Help in applet mode


2. Installation
===============
::

  $ sudo pip install wallpaperoptimzer


3. Uninstall
============
::

  $ sudo pip uninstall wallpaperoptimzer


4. Deployment directory
=======================
  Please see the setup.py.
 
  * At run time, I will create a log file of $HOME/.local/share/wallpaperoptimzer.
  * wallpaper file (For example, if you do not specify a save file name), It will be created in the $HOME/.local/share/wallpaperoptimzer.


5. Starting
===========
5.1 Execution example from Console
----------------------------------
  In advance, please install the file with $HOME/.local/share/wallpaperoptimzer/.walloptrc.
  If you do not plan to install, argument - designation of "1920x1080, 1280x1024 display" is required.

::

  $ wallpaperoptimizer 2560x1920.jpg 1500x844.jpg -C

Example)
~~~~~~~~
::

  1920x1080, left, ~/Wallpaper/1920/
  1280x1024, right, ~/Wallpaper/1280/


5.2 Wallpaper Changer run example from Console
----------------------------------------------
::

  $ wallpaperoptimizer -D -i 3600 &

5.3 Running as GNOME applet
---------------------------
  1. Right-click in any place of the GNOME panel, select "Add to Panel".
  2. Select "Wallpaperoptimizer Applet".

5.4 Running as App Indicator
----------------------------
  Depending on the path that has been installed, please proceed as follows:.

::

  $ /usr/local/bin/wallpaperoptimiz & 

  or

::

  $ /usr/bin/wallpaperoptimiz &


6. How to use
=============
6.1. Console
------------
  Refer to the Help.

::

  $ wallpaperoptimizer -h

6.2. Applet / Indicator app
---------------------------
  Button located in the main window to be started first will be the image that was placed to the left and right monitor.
  It becomes the specification for the entire workspace for margin.
  In addition, buttons arranged in the bottom of the main window is the operation buttons. You may not take effect until you do not do it by setting button.


7. Development environment
==========================

/etc/redhat-release
  Linux mint17

uname-r
  3.13.0-24-generic

likely associated ... deb
  * python-imaging
  * python-glade2
  * libglade2-0
  * python-gtk2

8. License
==========
  GPLv3

9. Use library
==============
The Python Imaging Library is:
    Copyright © 1997-2005 by Secret Labs AB
    Copyright © 1995-2005 by Fredrik Lundh

10. Change history
==================
v0.9.0.0 (2014.09.26) 0.9 release
---------------------------------
 - Support for Xfce4(4.10.1)

v0.8.2.0 (2014.04.07) 0.8 release
---------------------------------
 - Fixed a bug xfconf-query setting Xinerama-stretch

v0.8.1.0 (2013.08.10) 0.8 release
---------------------------------
 - registerd PyPI

v0.8.0.0 (2013.04.6) 0.8 release
--------------------------------
 - Support for Xfce4, LXDE
 - Create a new icon
 - Included with the desktop file

v0.7.0.1 (2013.02.12) 0.7 release
---------------------------------
 - Conducted internal change about the program structure

v0.6.0.0 (2013.02.12) 0.6 release
---------------------------------
 - GNOME3 desktop (Corresponding to the Ubuntu Unity)
 - Fixed a bug in the package distribution
 - Modifying configuration button behavior around

v0.5.0.0 (2012.10.7) 0.5 release
--------------------------------
 - Reduction in consideration of the case margin of the same size is not carried out, I fix the problem impossible to make margin

v0.4.0.0 (2012.8.6) 0.4 release
-------------------------------
 - When specifying only one screen, the improvement was the action to be suddenly wallpaper of various settings can not be.

v0.3.0.0 (2012.7.9) 0.3 No release
----------------------------------
 - The transition to development in python2.6 under
 - Support for x86_64 installation (/usr/lib64/...)

v0.2.0.0 (2012.2.1) release
---------------------------
 - first edition (Human Sacrifice version)


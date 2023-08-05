===========================
Raspberry Pi Smart-ish Door
===========================

.. WARNING::

  2014/05/13: this project is brand-spanking new, so it is most
  **definitely** not ready for use. Come back in a month or so.

.. IMPORTANT::

  IN CASE YOU MISSED THE "WARNING", THIS PROJECT IS CURRENTLY
  "PRE-ALPHA", WHICH MEANS IT DOES NOT WORK YET.

The `raspi-door` project comprises the GUI that is run on the
Raspberry PI on the inside of the door so that you can control your
door with *awesomeness*... or, as close as I can get it there.

But first you need to setup the hardware.


Raspi-Door Hardware
===================

TODO.


Raspi-Door Software
===================

.. code-block:: bash

  # create a virtualenv for raspi-door
  $ virtualenv --prompt '(raspi-door) ' /path/to/virtualenv
  $ . /path/to/virtualenv/bin/activate

  # install pre-requisites that have problems with pip...
  # TODO: figure out why this is necessary...
  $ easy_install pygame==1.9.1release



Credits
=======

* yuv2rgb_: Phil Burgess / Paint Your Dragon for Adafruit Industries
* picamera_: Dave Hughes


.. _yuv2rgb: https://github.com/adafruit/adafruit-pi-cam/blob/master/yuv2rgb.c
.. _picamera: https://pypi.python.org/pypi/picamera

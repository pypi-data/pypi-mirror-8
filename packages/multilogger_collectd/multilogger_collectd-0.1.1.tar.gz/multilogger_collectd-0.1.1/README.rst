arexx-multilogger-collectd-plugin
=================================

A `collectd <http://collectd.org>`__ plugin for AREXX Multiloggers.

AREXX Engineering (http://www.arexx.com/) produces data loggers for
monitoring temperature, humidity and CO2 levels. They consist of a base
station (BS-500) and multiple wireless sensors. The base station can be
connected to a PC over USB to download the data points and synchronize
clock.

However, all Linux support they provide is a single statically linked
binary, which can send data to a remote web server. This collectd plugin
is based on on the Arexx Data Logger Daemon written by Martin Mares who 
reverse-engineered the communication protocol. It also
uses code from the Python script of `Jörg
Rädler <http://www.j-raedler.de/2010/08/reading-arexx-tl-500-with-python-on-linux-part-ii/>`__.
See this
`post <http://rndhax.blogspot.ch/2010/03/friendlyarm-mini2440-arexx-tl-500.html>`__
for more links.

This program is not supported or endorsed by AREXX in any way.

Dependencies
------------

-  Python 2.4+
-  `PyUSB 1.0 <http://walac.github.io/pyusb/>`__
-  `collectd <http://collectd.org>`__ 4.9+

Install
-------

1. ``pip install multilogger_collectd``.
2. Configure the plugin (see below).
3. Restart collectd.

Configuration
-------------

Add the following to your collectd config (typically
/etc/collectd.conf):

.. code:: xml

    <LoadPlugin python>
        Globals true
    </LoadPlugin>

    <Plugin python>
        Import "multilogger_collectd.multilogger_collectd"

        <Module multilogger_collectd>
            <Sensor "9531">
                Name "9531-living-room"
                Offset 0
            </Sensor>
            <Sensor "9784">
                Name "9784-office"
                Offset -0.8
            </Sensor>
        </Module>
    </Plugin>

License
-------

This projected is licensed under the terms of the GPL v2.

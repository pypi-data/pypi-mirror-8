socle
=====

This is a simple yet modular SoC configuration utility, very much like
`raspi-config <http://elinux.org/RPi_raspi-config>`_ and others alike.
This one is written in Python and it aims to be extendable.
The name has no other meaning than it's a real word and it starts with SoC ;)


Features
--------

Preliminary support for following has been implemented:

* Configure hostname
* Configure timezone
* Configure wired/wireless network interfaces on Debian
* Switch off bells and whistles if it is used via UART


Boards
------

Following boards will be supported:

* Cubieboard2
* Cubietruck
* Raspberry Pi
* ZYBO
* Radxa

Debian jessie running on Cubietruck:

.. image:: http://lauri.vosandi.com/shared/soc-config/mainmenu-cubietruck.png

Raspbian running on Raspberry Pi:

.. image:: http://lauri.vosandi.com/shared/soc-config/mainmenu-raspi.png

Ubuntu 12.04 running on ZYBO:

.. image:: http://lauri.vosandi.com/shared/soc-config/mainmenu-zynq7000.png


Short term goals
----------------

As I have exams and other school assignments from the beginning until mid-July
I won't have much time to work on the short term goals but the last two days
of EuroPython 2014 is assigned to sprints and that's where I intend to finish all of the following
so feel free to join and help me out:

* Support u-boot configuration parsing, modifying
* Support /etc/modules parsing and modifying
* Support platform specific configuration editing, eg. video outputs, GPIO pins etc.
* Foolproofing UART connections, no fancy UI there
* Support configuring wired/wireless network interfaces
* Support configuring of remote management clients like Puppet and Salt minion
* Support configuring VPN clients like OpenVPN and StrongSwan


Long term goals
---------------

* Support Debian adoption on SoC-s
* Support for generating root filesystem images using debootstrap/febootstrap/arch-bootstrap etc
* Support for managing PL bitstream files


Author
------

`Lauri Võsandi <lauri.vosandi@gmail.com>`_ is embedded systems student currently pursuing his
master degree at Technical University of Berlin.
I am usually present at #linux-sunxi and #linux-rockchip channels on Freenode IRC as *lauri*,
that's also my registered nick there ;)
